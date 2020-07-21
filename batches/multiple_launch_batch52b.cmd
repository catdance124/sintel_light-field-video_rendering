::This is a batch script for launching multiple Blenders.
::    > .\run_batch.cmd
::    "../clean_files/scenes/05.2_bamboo/05.2b_comp.blend"

@echo off
cd ..
set file_path="../clean_files/scenes/05.2_bamboo/05.2b_comp.blend"
echo %file_path%
set start_frame=81
set end_frame=130

start "52b, 0 0 -> 0 8" powershell -Command "python .\run_blender.py %file_path% -resume '0 0' -end '0 8' -fs %start_frame% -fe %end_frame%"
start "52b, 1 0 -> 1 8" powershell -Command "python .\run_blender.py %file_path% -resume '1 0' -end '1 8' -fs %start_frame% -fe %end_frame%"
start "52b, 2 0 -> 2 8" powershell -Command "python .\run_blender.py %file_path% -resume '2 0' -end '2 8' -fs %start_frame% -fe %end_frame%"
start "52b, 3 0 -> 3 8" powershell -Command "python .\run_blender.py %file_path% -resume '3 0' -end '3 8' -fs %start_frame% -fe %end_frame%"
start "52b, 4 0 -> 4 8" powershell -Command "python .\run_blender.py %file_path% -resume '4 0' -end '4 8' -fs %start_frame% -fe %end_frame%"
start "52b, 5 0 -> 5 8" powershell -Command "python .\run_blender.py %file_path% -resume '5 0' -end '5 8' -fs %start_frame% -fe %end_frame%"
start "52b, 6 0 -> 6 8" powershell -Command "python .\run_blender.py %file_path% -resume '6 0' -end '6 8' -fs %start_frame% -fe %end_frame%"
start "52b, 7 0 -> 7 8" powershell -Command "python .\run_blender.py %file_path% -resume '7 0' -end '7 8' -fs %start_frame% -fe %end_frame%"
start "52b, 8 0 -> 8 8" powershell -Command "python .\run_blender.py %file_path% -resume '8 0' -end '8 8' -fs %start_frame% -fe %end_frame%"