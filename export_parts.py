import FreeCAD
import Part
import Mesh
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
        if obj.TypeId == 'PartDesign::Body':
            body_name = obj.Name
            shape = obj.Shape

            # STEP export
            step_path = os.path.join(out_dir, f"{body_name}.step")
            shape.exportStep(step_path)
            print(f"Exported STEP: {step_path}")

            # 3MF export
            mesh = Mesh.Mesh()
            mesh.addShape(shape)
            mesh_path = os.path.join(out_dir, f"{body_name}.3mf")
            mesh.write(mesh_path)
            print(f"Exported 3MF: {mesh_path}")

        else:
            print(f"Skipped: {obj.Name} ({obj.TypeId})")

    doc.close()
