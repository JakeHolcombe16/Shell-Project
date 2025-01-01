A Unix-like operating system replication. Using a tree data structure to represent the file systems.
Shell Operations
cd <name of directory>: "Change directory."  Move to the new directory. The special directory .. (two periods) is the parent directory of whatever folder you're in.

ls: "List." Lists all the files and folders in the current directory.

touch <filename>: Make a new empty file with the given name.

mkdir <directory name>: Make a new empty directory with the given name.

pwd: "Present working directory." Ouput the path to the current directory, starting with the root.

rm <filename>: Remove a file.  An error occurs if rm is used on a directory name.

rmdir <directory name>: Remove an EMPTY directory. An error occurs if rmdir is used on a file or a non-empty directory.

tree: Pretty-print the contents of this directory recursively using a pre-order traversal with the current directory as the root.  The level a node is on determines the number of tabs preceding it.
