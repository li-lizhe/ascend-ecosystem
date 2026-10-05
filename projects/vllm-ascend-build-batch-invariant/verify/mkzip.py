import zipfile, os
D = os.path.dirname(os.path.abspath(__file__))
z = zipfile.ZipFile(os.path.join(D, "whl.zip"), "w")
z.writestr("torch_ops_extension/batch_invariant_ops/build_and_install.sh",
           "#!/bin/bash\necho '[stub build_and_install] ok'\nexit 0\n")
z.close()
print("wrote", os.path.join(D, "whl.zip"))
