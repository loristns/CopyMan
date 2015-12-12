import shutil
import sys
import os
import datetime
import tarfile

def copy_file(src, dest):
    """Simple function to copy files or directory"""
    dest_file = os.path.split(src)
    try:
        dest_eval = os.path.join(dest, dest_file[1])
        try:
            shutil.copyfile(src, dest_eval)
            return 'ok'
        #src and dest are the same file
        except shutil.Error:
            print 'Error : Source and Destination are the same file.'
            return 'oups'
        #src or dest doesn't exist
        except IOError as e:
            print 'Log : ' + str(e)
            try:
                shutil.copytree(src, dest_eval)
                return 'ok'
                #src and dest are the same file
            except shutil.Error:
                print 'Error : Source and Destination are the same file.'
                return 'oups'
	        #src or dest doesn't exist
            except IOError as e:
                print 'Log : ' + str(e)
                return 'oups'
    except IndexError:
        dest_eval = dest
        try:
            shutil.copytree(src, dest_eval)
            return 'ok'
        #src and dest are the same file
        except shutil.Error:
            print 'Error : Source and Destination are the same file.'
            return 'oups'
	    #src or dest doesn't exist
        except IOError as e:
            print 'Log : ' + str(e)
            return 'oups'
		

def copy_lot_file(srclst, to):
    """An extension to copy_file() to allow you to copy lot of files."""
    print 'Copying files, please wait...'
    for copy in srclst:
        log = copy_file(copy, to)
        if log == 'ok':
            print 'Copying successful'
		
def generate_namefile():
    """A simple function who return the name of the tar.gz file."""
    today = datetime.date.today()
    return str(today) + "-Package.tar.gz"
	
def targz_file(srclst, name):
    """Function who compress in a tar.gz file some other files."""
    print 'Compressing files, please wait...'
    targz =  tarfile.open(name, "w:gz")
    for file in srclst:
        targz.add(file)
    targz.close()
	
def help(error=False):
    if error:
        print "Unrecognized command, see help here."

    print " Commands :"
    print ""
    print "python copyman.py help : to get help"
    print ""
    print "python copyman.py copy <destination> <source1> <source2> <source3> ... : to copy a list of files/directories in an unique directory"
    print ""
    print "python copyman.py tar <destination> <source1> <source2> <source3> ... :  to compress (tar.gz) a list of files/directories in an unique file."

command = sys.argv[1]
if command == "help":
    help()
elif command == "copy":
    copy_lot_file(sys.argv[3:], sys.argv[2])
elif command == "tar":
    targz_file(sys.argv[3:], sys.argv[2] +"/"+ generate_namefile())
else:
    help(error=True)
