import FreeCAD
import MeshPart
import os
import glob

output_root = "exports"
os.makedirs(output_root, exist_ok=True)

for fc_file in glob.glob("*.FCStd"):
    print(f"🔍 Processing: {fc_file}")
    doc = FreeCAD.openDocument(fc_file)
    FreeCAD.setActiveDocument(doc.Name)
    FreeCAD.ActiveDocument.recompute()

    file_base = os.path.splitext(os.path.basename(fc_file))[0]
    out_dir = os.path.join(output_root, file_base)
    os.makedirs(out_dir, exist_ok=True)

    for obj in doc.Objects:
        if obj.TypeId == 'PartDesign::Body' and hasattr(obj, "Shape"):
            shape = obj.Shape
            if not shape.isNull():
                # Sanitize the object name for safe filenames if needed
                obj_name_safe = obj.Name.replace(" ", "_")
                out_file = os.path.join(out_dir, f"{obj_name_safe}.stl")

                mesh = MeshPart.meshFromShape(
                    Shape=shape,
                    LinearDeflection=0.1,
                    AngularDeflection=15
                )
                mesh.write(out_file)
                print(f"✅ Exported: {out_file}")
            else:
                print(f"⚠️ Skipped null shape: {obj.Name}")
        else:
            print(f"⏩ Skipped: {obj.Name} ({obj.TypeId})")

    doc.close()
