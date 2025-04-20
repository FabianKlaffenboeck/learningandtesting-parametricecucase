import FreeCAD
import MeshPart
import os
import glob

output_root = "exports"
os.makedirs(output_root, exist_ok=True)

for fc_file in glob.glob("*.FCStd"):
    print(f"Processing {fc_file}")
    doc = FreeCAD.openDocument(fc_file)
    FreeCAD.setActiveDocument(doc.Name)
    FreeCAD.ActiveDocument.recompute()

    file_base = os.path.splitext(os.path.basename(fc_file))[0]
    out_dir = os.path.join(output_root, file_base)
    os.makedirs(out_dir, exist_ok=True)

    for obj in doc.Objects:
        if obj.TypeId == 'PartDesign::Body':
            shape = obj.Shape
            if not shape.isNull():
                stl_file = os.path.join(out_dir, f"{obj.Name}.stl")
                mesh = MeshPart.meshFromShape(
                    Shape=shape,
                    LinearDeflection=0.1,
                    AngularDeflection=15,
                    Relative=False
                )
                mesh.write(stl_file)
                print(f"Exported body to STL: {stl_file}")
            else:
                print(f"Skipped null shape: {obj.Name}")
        else:
            print(f"Skipped: {obj.Name} ({obj.TypeId})")

    doc.close()
