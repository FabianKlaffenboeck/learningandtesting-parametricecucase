import FreeCAD
import Part
import os
import glob

output_root = "exports"
os.makedirs(output_root, exist_ok=True)

for fc_file in glob.glob("*.FCStd"):
    print(f"Processing {fc_file}")
    doc = FreeCAD.openDocument(fc_file)
    FreeCAD.setActiveDocument(doc.Name)

    file_base = os.path.splitext(os.path.basename(fc_file))[0]
    out_dir = os.path.join(output_root, file_base)
    os.makedirs(out_dir, exist_ok=True)

    for obj in doc.Objects:
        # Only export PartDesign Bodies
        if obj.TypeId == 'PartDesign::Body':
            shape = obj.Shape
            out_file = os.path.join(out_dir, f"{obj.Name}.step")
            shape.exportStep(out_file)
            print(f"Exported body: {out_file}")
        else:
            print(f"Skipped: {obj.Name} ({obj.TypeId})")

    doc.close()
