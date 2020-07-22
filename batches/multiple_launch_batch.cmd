::This is a batch script for launching multiple Blenders.
::    > .\run_batch.cmd
::    "../clean_files/scenes/05.2_bamboo/05.2b_comp.blend"

@echo off
cd ..
set file_path="../clean_files/scenes/03.1_alley/03.1e_comp.blend"
echo %file_path%
set start_frame=11
set end_frame=61

start "0" python .\run_blender.py %file_path% -resume "0 0" -end "0 8" -fs %start_frame% -fe %end_frame%
start "1" python .\run_blender.py %file_path% -resume "1 0" -end "1 8" -fs %start_frame% -fe %end_frame%
start "2" python .\run_blender.py %file_path% -resume "2 0" -end "2 8" -fs %start_frame% -fe %end_frame%
start "3" python .\run_blender.py %file_path% -resume "3 0" -end "3 8" -fs %start_frame% -fe %end_frame%
start "4" python .\run_blender.py %file_path% -resume "4 0" -end "4 8" -fs %start_frame% -fe %end_frame%
start "5" python .\run_blender.py %file_path% -resume "5 0" -end "5 8" -fs %start_frame% -fe %end_frame%
start "6" python .\run_blender.py %file_path% -resume "6 0" -end "6 8" -fs %start_frame% -fe %end_frame%
start "7" python .\run_blender.py %file_path% -resume "7 0" -end "7 8" -fs %start_frame% -fe %end_frame%
start "8" python .\run_blender.py %file_path% -resume "8 0" -end "8 8" -fs %start_frame% -fe %end_frame%