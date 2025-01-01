"""
    Filename: holcombe_project5.py
    Author: Jake Holcombe
    Date: 6/9/2023
    Course: COMP 1353
    Assignment: Project 5 - File System Tree
    Collaborators: None
    Internet Source: None
"""
import pickle
class TreeNode:
    # Instace Vars
    def __init__(self,name:str,parent,is_directory:bool) -> None:
        self.name = name
        self.children = []
        self.parent = parent
        self.is_directory = is_directory
    # Return if the parent is none meaning it is the root
    def is_root(self):
        return self.parent is None
    
    # Append a child to the children list
    def append_child(self,name, is_directory):
        return self.children.append(TreeNode(name,self.parent,is_directory))
        
    
    
    def __str__(self) -> str:
        if self.is_directory:
            return f"{self.name} <directory>"
        else:
            return self.name

class FileSystem:
    # Initialize our root
    def __init__(self) -> None:
        self.root = TreeNode('Root',None,True)
        self.current_directory = self.root

    # Helper method to help us check if a file or directory is already in the currrent directory
    def _check_make_file(self,name):
        # Loop through our current_directory's children
        for ele in self.current_directory.children:
            # Check if the elements name is the same as the name passed in
            if name in ele.name:
                print(f"{name} is already in the directory {self.current_directory}")
                return False
        return True
    
    def ls(self):
        return_result = ''
        # looping through the children and adding that the return result and return the string
        for name in self.current_directory.children:
            return_result += str(name) + ' '
        return return_result

    # Check if the name already exists otherwise append it to the list of the current directory's children and set the is_directory to False
    def touch(self,name):
        if not self._check_make_file(name):
            return
        else:
            self.current_directory.children.append(TreeNode(name,self.current_directory,False))

    # Check if the name already exists otherwise append it to the list of the current directory's children and set the is_directory to True
    def mkdir(self, dirname):
        if not self._check_make_file(dirname):
            return
        else:
            self.current_directory.children.append(TreeNode(dirname,self.current_directory,True))
    
    # Check if the user wants to go back first by checking ..
    def cd(self, name):
        
        if name == '..':
            # Check if they are already at the root
            if self.current_directory.is_root():
                print("Already at root, cannot go back")
                return
            # make the current directory the parent
            else:
                self.current_directory = self.current_directory.parent
                return
        # find the element in the children and if its a directory change into that directory otherwise, that means its a file so print the error
        for e in self.current_directory.children:
            if e.name == name:
                if e.is_directory:
                    self.current_directory = e
                    return
                else:
                    print(f'{name} is not a directory, cannot change into a file')
                    return
        # If the loop finishs then the name isn't in the directory
        else:
            print(f'{name} is not in {self.current_directory}')
            return
    
            
    def rm(self,filename):
        # Loop through the children
        for i in range(len(self.current_directory.children)):
            # If the element at the index is the filename
            if self.current_directory.children[i].name == filename:
                # Check if it is a directory and notify them that they need to use rmdir
                if self.current_directory.children[i].is_directory:
                    print("Cannot remove a directory with rm, use rmdir")
                    return
                # Otherwise we pop the child at the index
                else:
                    self.current_directory.children.pop(i)
                    return
        # If the file is not in the directory
        print(f"{filename} is not in current directory")
    
    def rmdir(self, dirname):
        for i in range(len(self.current_directory.children)):
            if self.current_directory.children[i].name == dirname:
                
                if not self.current_directory.children[i].is_directory:
                    print("Cannot remove a file with rmdir, use rm")
                    return
                elif len(self.current_directory.children[i].children) > 0:
                    print("Cannot remove a directory with data in it")
                    return
                else:
                    self.current_directory.children.pop(i)
                    return
                

        print(f"{dirname} not in current directory")
    
    # Call the recursive tree helper that the level starts at 0
    def tree(self):
        self.recur_tree(0)

    def recur_tree(self,l):
        # define our tab level
        tab = l*'\t'
        # print our tab(recursive tab) and add the current directory we are in
        print(tab+str(self.current_directory))
        # Loop through the children of the current directory
        for element in self.current_directory.children:
            # If the element is a directory we will change that to the current directory, then recursively call the function to add an extra tab
            if element.is_directory:
                self.current_directory = element
                self.recur_tree(l+1)
            # Otherwise we will just print the elements on the same tab level
            else:
                print(tab+"\t"+str(element))
    
    # Start with / and loop through all the directorys until we get to the root and add them to the return_result and return the result
    def pwd(self):
        return_result = '/'
        return_result += str(self.current_directory) + '/ '
        while self.current_directory.parent is not None:
            self.current_directory = self.current_directory.parent
            return_result += str(self.current_directory) + '/ '
        return return_result
    
# main driver
def main():
    filesys = FileSystem()
    # Code provided from assignment
    try:
        with open("file_system.bin", "rb") as file_source:
            file_system = pickle.load(file_source)
            print("File System loaded")
    except:
        print("Creating a new file system: file doesn't exist or data file is out of date because FileSystem class changed")
        file_system = FileSystem()
    with open("file_system.bin", "wb") as file_destination:
        pickle.dump(file_system, file_destination)
        print("File system saved")

    # Console loop
    message = ''
    while message != 'quit':
        # We take the inputted message we lower and split the string into a list so it would look like ['cd', '<directory>'] and we can target those values
        message = input('').lower().split(' ')
        # Check all of the methods that dont require a second input
        if message[0] == 'pwd':
            print(filesys.pwd())
        elif message[0] == 'ls':
            print(filesys.ls())
        elif message[0] == 'tree':
            # This method already prints so we dont need to print it
            filesys.tree()
        # We need to add a try except, if the user types "rm" there is no message[1] so the program crashes
        elif message[0] == 'rm':
            try:
                # We pass in the message[1] which should be the file
                filesys.rm(message[1])
            except IndexError:
                print('No filename was provided (Index out of range)')
        elif message[0] == 'rmdir':
            try:
                # Pass in the directory
                filesys.rmdir(message[1])
            except IndexError:
                print('No directory was provided (Index out of range)')
        elif message[0] == 'mkdir':
            try:
                # Pass in the name
                filesys.mkdir(message[1])
            except IndexError:
                print('No directory name was provided (Index out of range)')
        elif message[0] == 'touch':
            try:
                # Pass in the name
                filesys.touch(message[1])
            except IndexError:
                print("No file name was provided (index out of range)")
        elif message[0] == 'cd':
            try:
                # Pass in the directory
                filesys.cd(message[1])
            except IndexError:
                print("No directory was profided, (Index out of range)")
        # Added a help message board incase someone doesn't know how to use it
        elif message[0] == 'help':
            print('pwd - print the name of the path starting from the root')
            print('tree - prints the tree rooted at the current directory')
            print('ls - prints all the items in the current directory')
            print('cd <dirname> - changes directory to the dirname in the current directory, use ".." to go back a directory')
            print("rm <filename> - removes a file in the current directory")
            print("rmdir <dirname> - removes a directory as long as its empty in the current directory")
            print("touch <filename> - creates a file in the current directory")
            print("mkdir <dirname> - creates a directory in the current directory")
        # Quit the program
        elif message[0] == 'quit':
            break
        # If input isn't recognized
        else:
            print('input not recognized, type "help" for commands')
main()