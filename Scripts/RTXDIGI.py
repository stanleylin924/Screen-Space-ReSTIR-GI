from falcor import *

def render_graph_RTXDIGI():
    g = RenderGraph("RTXDIGI")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary("RTXDIPass.dll")
    loadRenderPassLibrary("RTXGIPass.dll")
    loadRenderPassLibrary("GlobalIlluminationPass.dll")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("ToneMapper.dll")
    VBufferRT = createPass("VBufferRT")
    g.addPass(VBufferRT, "VBufferRT")
    RTXDIPass = createPass("RTXDIPass")
    g.addPass(RTXDIPass, "RTXDIPass")
    GBuffer = createPass("GBufferRaster")
    g.addPass(GBuffer, "GBuffer")
    RTXGIPass = createPass("RTXGIPass", {'useVBuffer': False})
    g.addPass(RTXGIPass, "RTXGIPass")
    GlobalIlluminationPass = createPass("GlobalIlluminationPass")
    g.addPass(GlobalIlluminationPass, "GlobalIlluminationPass")
    AccumulatePass = createPass("AccumulatePass", {'enabled': False, 'precisionMode': AccumulatePrecision.Single})
    g.addPass(AccumulatePass, "AccumulatePass")
    ToneMappingPass = createPass("ToneMapper", {'autoExposure': False, 'exposureCompensation': 0.0})
    g.addPass(ToneMappingPass, "ToneMappingPass")
    g.addEdge("VBufferRT.vbuffer", "RTXDIPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "RTXDIPass.mvec")
    g.addEdge("GBuffer.posW", "RTXGIPass.posW")
    g.addEdge("GBuffer.normW", "RTXGIPass.normalW")
    g.addEdge("GBuffer.tangentW", "RTXGIPass.tangentW")
    g.addEdge("GBuffer.faceNormalW", "RTXGIPass.faceNormalW")
    g.addEdge("GBuffer.texC", "RTXGIPass.texC")
    g.addEdge("GBuffer.texGrads", "RTXGIPass.texGrads") # This input is optional
    g.addEdge("GBuffer.mtlData", "RTXGIPass.mtlData")
    g.addEdge("GBuffer.depth", "RTXGIPass.depth") # This input is optional

    g.addEdge("RTXDIPass.color", "GlobalIlluminationPass.diColor")
    g.addEdge("RTXGIPass.output", "GlobalIlluminationPass.giColor")
    g.addEdge("GlobalIlluminationPass.color", "AccumulatePass.input")
    g.addEdge("AccumulatePass.output", "ToneMappingPass.src")

    g.markOutput("ToneMappingPass.dst")
    g.markOutput("AccumulatePass.output")
    g.markOutput("RTXDIPass.color")
    g.markOutput("RTXGIPass.output")
    return g

RTXDIGI = render_graph_RTXDIGI()
try: m.addGraph(RTXDIGI)
except NameError: None
