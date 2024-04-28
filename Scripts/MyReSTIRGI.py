from falcor import *

def render_graph_ReSTIRGI():
    g = RenderGraph("ReSTIRGI")
    loadRenderPassLibrary("AccumulatePass.dll")
    loadRenderPassLibrary("GBuffer.dll")
    loadRenderPassLibrary('ReSTIRGIGBuffer.dll')
    loadRenderPassLibrary("MyReSTIRGIPass.dll")
    loadRenderPassLibrary("RTXDIPass.dll")
    loadRenderPassLibrary("GlobalIlluminationPass.dll")
    loadRenderPassLibrary("ToneMapper.dll")

    VBufferRT = createPass("VBufferRT")
    g.addPass(VBufferRT, "VBufferRT")

    ReSTIRGIGBuffer = createPass('ReSTIRGIGBuffer', {'maxBounces': 1, 'useImportanceSampling': True})
    g.addPass(ReSTIRGIGBuffer, 'ReSTIRGIGBuffer')

    MyReSTIRGIPass = createPass("MyReSTIRGIPass")
    g.addPass(MyReSTIRGIPass, "MyReSTIRGIPass")

    RTXDIPass = createPass("RTXDIPass")
    g.addPass(RTXDIPass, "RTXDIPass")

    GlobalIlluminationPass = createPass("GlobalIlluminationPass")
    g.addPass(GlobalIlluminationPass, "GlobalIlluminationPass")

    AccumulatePass = createPass("AccumulatePass", {'enabled': False, 'precisionMode': AccumulatePrecision.Single})
    g.addPass(AccumulatePass, "AccumulatePass")

    ToneMapper = createPass("ToneMapper", {'autoExposure': False, 'exposureCompensation': 0.0})
    g.addPass(ToneMapper, "ToneMapper")

    g.addEdge('VBufferRT.vbuffer', 'ReSTIRGIGBuffer.vbuffer')
    g.addEdge('VBufferRT.viewW', 'ReSTIRGIGBuffer.viewW')

    g.addEdge("ReSTIRGIGBuffer.vPosW", "MyReSTIRGIPass.vPosW")
    g.addEdge("ReSTIRGIGBuffer.vNormW", "MyReSTIRGIPass.vNormW")
    g.addEdge("ReSTIRGIGBuffer.random", "MyReSTIRGIPass.random")
    g.addEdge("ReSTIRGIGBuffer.sPosW", "MyReSTIRGIPass.sPosW")
    g.addEdge("ReSTIRGIGBuffer.sNormW", "MyReSTIRGIPass.sNormW")
    g.addEdge("ReSTIRGIGBuffer.vColor", "MyReSTIRGIPass.vColor")
    g.addEdge("ReSTIRGIGBuffer.sColor", "MyReSTIRGIPass.sColor")

    g.addEdge("VBufferRT.vbuffer", "MyReSTIRGIPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "MyReSTIRGIPass.motionVectors")

    g.addEdge("VBufferRT.vbuffer", "RTXDIPass.vbuffer")
    g.addEdge("VBufferRT.mvec", "RTXDIPass.mvec")

    g.addEdge("RTXDIPass.color", "GlobalIlluminationPass.diColor")
    g.addEdge("MyReSTIRGIPass.color", "GlobalIlluminationPass.giColor")

    g.addEdge("GlobalIlluminationPass.color", "AccumulatePass.input")

    g.addEdge("AccumulatePass.output", "ToneMapper.src")

    g.markOutput("ToneMapper.dst")
    g.markOutput("AccumulatePass.output")
    g.markOutput("GlobalIlluminationPass.color")
    g.markOutput("RTXDIPass.color")
    g.markOutput("MyReSTIRGIPass.color")
    g.markOutput('ReSTIRGIGBuffer.vPosW')
    g.markOutput('ReSTIRGIGBuffer.vNormW')
    g.markOutput('ReSTIRGIGBuffer.vColor')
    g.markOutput('ReSTIRGIGBuffer.random')
    g.markOutput('ReSTIRGIGBuffer.sPosW')
    g.markOutput('ReSTIRGIGBuffer.sNormW')
    g.markOutput('ReSTIRGIGBuffer.vColor')
    g.markOutput('ReSTIRGIGBuffer.sColor')

    return g

ReSTIRGI = render_graph_ReSTIRGI()
try: m.addGraph(ReSTIRGI)
except NameError: None

# m.setMogwaiUISceneBuilderFlag(buildFlags = SceneBuilderFlags.UseCompressedHitInfo)

# m.loadScene('Arcade\Arcade.pyscene')
m.loadScene('../Data/pink_room/pink_room.pyscene')
# m.loadScene('../Data/VeachAjar/VeachAjar.pyscene')
# m.loadScene('../Data/VeachAjar/VeachAjarAnimated.pyscene')
