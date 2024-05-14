/***************************************************************************
 # Copyright (c) 2015-21, NVIDIA CORPORATION. All rights reserved.
 #
 # NVIDIA CORPORATION and its licensors retain all intellectual property
 # and proprietary rights in and to this software, related documentation
 # and any modifications thereto.  Any use, reproduction, disclosure or
 # distribution of this software and related documentation without an express
 # license agreement from NVIDIA CORPORATION is strictly prohibited.
 **************************************************************************/
#pragma once
#include "Falcor.h"
#include "RenderGraph/RenderPassHelpers.h"
#include "Rendering/ReSTIRGI/ScreenSpaceReSTIR.h"

#define INITIAL_SAMPLING (1)

using namespace Falcor;

class ReSTIRGIPass : public RenderPass
{
public:
    using SharedPtr = std::shared_ptr<ReSTIRGIPass>;

    static const Info kInfo;

    /** Create a new render pass object.
        \param[in] pRenderContext The render context.
        \param[in] dict Dictionary of serialized parameters.
        \return A new object, or an exception is thrown if creation failed.
    */
    static SharedPtr create(RenderContext* pRenderContext = nullptr, const Dictionary& dict = {});

    virtual Dictionary getScriptingDictionary() override;
    virtual RenderPassReflection reflect(const CompileData& compileData) override;
    virtual void compile(RenderContext* pRenderContext, const CompileData& compileData) override;
    virtual void execute(RenderContext* pRenderContext, const RenderData& renderData) override;
    virtual void renderUI(Gui::Widgets& widget) override;
    virtual void setScene(RenderContext* pRenderContext, const Scene::SharedPtr& pScene) override;
    virtual bool onMouseEvent(const MouseEvent& mouseEvent) override;
    virtual bool onKeyEvent(const KeyboardEvent& keyEvent) override { return false; }

private:
    ReSTIRGIPass(const Dictionary& dict);

    void parseDictionary(const Dictionary& dict);

    void prepareSurfaceData(RenderContext* pRenderContext, const Texture::SharedPtr& pVBuffer, size_t instanceID);
#if INITIAL_SAMPLING
    void initialSample(
        RenderContext* pRenderContext,
        const Texture::SharedPtr& pVPosW,
        const Texture::SharedPtr& pVNormW,
        const Texture::SharedPtr& pSPosW,
        const Texture::SharedPtr& pSNormW,
        const Texture::SharedPtr& pSColor,
        const Texture::SharedPtr& pRandom,
        size_t instanceID
    );
#endif
    void finalShading(RenderContext* pRenderContext, const Texture::SharedPtr& pVBuffer, const RenderData& renderData, size_t instanceID);

    void updateDict(const Dictionary& dict);

    // Internal state
    Scene::SharedPtr mpScene;
    std::vector<ScreenSpaceReSTIR::SharedPtr> mpScreenSpaceReSTIR;
    ScreenSpaceReSTIR::Options mOptions;
    bool mOptionsChanged = false;
    uint2 mFrameDim = uint2(0);
    bool mGBufferAdjustShadingNormals = false;

    ComputePass::SharedPtr mpPrepareSurfaceData;
#if INITIAL_SAMPLING
    ComputePass::SharedPtr mpInitialSampling;
#endif
    ComputePass::SharedPtr mpFinalShading;

    int mNumReSTIRInstances = 1;
    bool mNeedRecreateReSTIRInstances = false;

    bool                        mComputeDirect = true;          ///< Compute direct illumination (otherwise indirect only).
};
