/***************************************************************************
 # Copyright (c) 2015-21, NVIDIA CORPORATION. All rights reserved.
 #
 # NVIDIA CORPORATION and its licensors retain all intellectual property
 # and proprietary rights in and to this software, related documentation
 # and any modifications thereto.  Any use, reproduction, disclosure or
 # distribution of this software and related documentation without an express
 # license agreement from NVIDIA CORPORATION is strictly prohibited.
 **************************************************************************/
import LoadShadingData;
import Utils.Color.ColorHelpers;
import Rendering.ReSTIRGI.ScreenSpaceReSTIR;

/** Prepares ReSTIR surface data.
*/
struct PrepareSurfaceData
{
    Texture2D<PackedHitInfo> vbuffer;

    uint2 frameDim;

    void execute(uint2 pixel)
    {
        if (any(pixel >= frameDim)) return;

        ShadingData sd;

        // loadShadingData() 會呼叫到 Falcor 的 prepareShadingData()，但是這版 Falcor 的 prepareShadingData()
        // 必須傳入一個 ITextureSampler 紋理採樣器。所以，透過 ExplicitLodTextureSampler() 先取得一個紋理採樣器。
        // ExplicitLodTextureSampler() 的參數為 texture level-of-detail，目前固定傳入 0.0f，表示取得最高細節級別
        // 的紋理採樣器。未來可改為動態計算適當的 LOD 級別。
        let lod = ExplicitLodTextureSampler(0.f); // TODO: Implement texture level-of-detail.

        bool isValidSurface = loadShadingData(pixel, frameDim, gScene.camera, vbuffer, lod, sd);

        if (isValidSurface)
        {
            // 當前像素點落在物體表面上，有效的 shading data 載入存放於 sd 變數中。

            // 從場景的材質系統中獲取當前表面點對應的 BSDF 物件，並從該 BSDF 物件中提取出一些需要的材質屬性。
            // gScene 是當前渲染場景的物件，gScene.materials 是場景中用於管理所有材質的子物件。
            // getBSDF(sd, lod) 根據傳入的 ShadingData sd (包含表面點的各種著色資訊) 和 lod (紋理採樣器)
            // 來獲取對應的 BSDF 物件。此 BSDF 物件包含了該表面點的完整 BSDF 資訊。
            let bsdf = gScene.materials.getBSDF(sd, lod);
            // 從該 BSDF 物件中提取出一些關鍵的材質屬性參數。
            let bsdfProperties = bsdf.getProperties(sd);

            // 計算相機到 shading point 的距離，gScene.camera.getPosition() 是相機的世界座標，
            // sd.posW 是 shading point 的世界座標。
            float depth = distance(gScene.camera.getPosition(), sd.posW);

            // 從當前材質的 BSDF 屬性中計算漫反射權重，這版 Falcor 的 ShadingData 已經沒有儲存 diffuse，
            // 因此無法直接讀取 sd.diffuse。
            float diffuseWeight = luminance(bsdfProperties.diffuseReflectionAlbedo);

            // 從當前材質的 BSDF 屬性中計算鏡面反射權重，這版 Falcor 的 ShadingData 已經沒有儲存 specular，
            // 因此無法直接讀取 sd.specular。
            float specularWeight = luminance(bsdfProperties.specularReflectance);

            // 這版 Falcor 的 ShadingData 已經沒有儲存 roughness，因此無法直接讀取 sd.linearRoughness。
            // 透過呼叫 setSurfaceData 函數，將這些參數傳遞給 gScreenSpaceReSTIR 物件，
            // 意味著將當前像素點的表面屬性資訊注入到 ReSTIR 演算法的計算管線中，為 ReSTIR 提供所需的表面屬性。
            gScreenSpaceReSTIR.setSurfaceData(pixel, sd.computeNewRayOrigin(), depth, sd.N, sd.faceN, diffuseWeight, specularWeight, bsdfProperties.roughness);
        }
        else
        {
            // 當前像素點未落在物體表面上，sd 變數中的 shading data 無效。
            gScreenSpaceReSTIR.setInvalidSurfaceData(pixel);
        }
    }
};

ParameterBlock<PrepareSurfaceData> gPrepareSurfaceData;

[numthreads(16, 16, 1)]
void main(uint3 dispatchThreadId : SV_DispatchThreadID)
{
    gPrepareSurfaceData.execute(dispatchThreadId.xy);
}
