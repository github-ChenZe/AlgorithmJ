from jpype import *
import jpype as jp
import PIL.Image as Image
import io
import profile


def showDiagram():
    profile.fire()
    xml = """<?xml version="1.0" encoding="utf-8" ?>
<table>
    <row>
        <table>
            <row>
                <cell>First</cell>
                <cell>Second</cell>
            </row>
        </table>
        <cell>Python</cell>
    </row>
    <row>
        <cell>Speed</cell>
        <cell>Slow</cell>
    </row>
</table>
    """
    arr = reader.newBytes(len(xml))
    for i in range(0, len(xml)):
        arr[i] = JByte(ord(xml[i]))
        print arr[i]
    print "OK"
    rgba = reader.toDiagram(arr)
    profile.check()
    length = len(rgba)
    b = bytearray(length)
    for i in range(0, length):
        b[i] = (rgba[i] & 0xff)
    image = Image.open(io.BytesIO(b))
    image.show()


if __name__ == '__main__':
    classpath = "/Users/zechen/Intellij/AlgorithmGraphic/out/artifacts/AlgorithmGraphic_jar/AlgorithmGraphic.jar"
    jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath)
    reader = jp.JPackage("XMLReader").XMLReader
    raw_input('>>> ')
    showDiagram()

    shutdownJVM()
