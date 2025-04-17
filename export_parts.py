import FreeCAD
import Part
import glob
import os

fc_files = glob.glob("*.FCStd")

if not fc_files:
    print("No .FCStd files found.")
    exit(1)

output_root = "exports"
os.makedirs(output_root, exist_ok=True)

for fc_file in fc_files:
    print(f"Processing: {fc_file}")
    doc = FreeCAD.openDocument(fc_file)
    FreeCAD.setActiveDocument(doc.Name)

    file_base = os.path.splitext(os.path.basename(fc_file))[0]
    out_dir = os.path.join(output_root, file_base)
    os.makedirs(out_dir, exist_ok=True)

    for obj in doc.Objects:
        if hasattr(obj, "Shape"):
            shape = obj.Shape
            out_file = os.path.join(out_dir, f"{obj.Name}.step")
            shape.exportStep(out_file)
            print(f"Exported: {out_file}")

    doc.close()
