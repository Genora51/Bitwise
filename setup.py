from cx_Freeze import setup, Executable

target = Executable(
    script="bitwise.py",
    base="Console",
    icon="dist/binary.ico"
    )

setup(
    name="name",
    version="0.1.0",
    description="Bitwise Language",
    author="Geno Racklin Asher",
    options={
    	'build_exe': {
	        'includes': ['lib'],
	    }
    },
    executables=[target]
    )
