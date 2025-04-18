import FreeCAD
import MeshPart
import os
import glob

output_root = "exports"
os.makedirs(output_root, exist_ok=True)

for fc_file in glob.glob("*.FCStd"):
    print(f"\n🔍 Processing file: {fc_file}")
    doc = FreeCAD.openDocument(fc_file)
    FreeCAD.setActiveDocument(doc.Name)
    FreeCAD.ActiveDocument.recompute()

    file_base = os.path.splitext(os.path.basename(fc_file))[0]
    out_dir = os.path.join(output_root, file_base)
    os.makedirs(out_dir, exist_ok=True)

    exported = False

    for obj in doc.Objects:
        print(f"  - Found: {obj.Name} ({obj.TypeId})")
        if obj.TypeId == 'PartDesign::Body' and hasattr(obj, 'Shape'):
            shape = obj.Shape
            if not shape.isNull():
                body_name = obj.Name
                mesh_path = os.path.join(out_dir, f"{body_name}.stl")

                # Use MeshPart to generate mesh and export
                mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=15)
                mesh.write(mesh_path)
                print(f"    ✅ Exported STL: {mesh_path}")
                exported = True
            else:
                print(f"    ⚠️ Null shape: {obj.Name}")
        else:
            print(f"    ❌ Skipped: {obj.Name} ({obj.TypeId})")

    doc.close()

    if not exported:
        print(f"⚠️ No valid STL exports in: {fc_file}")
