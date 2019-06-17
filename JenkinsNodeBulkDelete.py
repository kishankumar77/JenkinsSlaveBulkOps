#/usr/bin/python3.6

### Modules Imports
import sys, getopt
import subprocess
import os

### Global Variables 
JENKINS_CLI = "/usr/bin/jenkins-cli.jar"
ScriptInput = {}

def ProcessInputs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:s:a:n:", [ "help", "jenkinsserver=", "auth=", "nodes=" ]) 
    except getopt.GetoptError:
        Usage()
        sys.exit(2)

    for opt, arg in opts:
        print("options is %s,%s\n" %(opt, arg) )
        if opt in ('-h', '--help'):
            Usage()
            sys.exit(3)
        elif opt in ('-s', '--jenkinsserver'):
            ScriptInput['jenkinsserver'] = arg
        elif opt in ('-a', '--auth'):
            ScriptInput['auth'] = arg
        elif opt in ('-n', '--nodes'):
            ScriptInput['nodes'] = arg
        else:
            print( "wrong option input\n" )
            Usage()
    print(ScriptInput)
   
    if 'jenkinsserver' not in ScriptInput:
        print( "jenkinsserver option is mandatory\n" )
        Usage()

    if 'auth' not in ScriptInput:
        print( "auth option is mandatory\n" )
        Usage()

    if 'nodes' not in ScriptInput:
        print( "nodes option is mandatory\n" )
        Usage()
        
def DeleteSlaves():
    print( "Deleting Slave(s) from Jenkins \n" )

    Nodes = ScriptInput['nodes'].split(",")

    for node in Nodes:
        print( "Deleting node: {0}".format(node))
            print( " Running Jenkins delete-node command to delete slave\n" )
            result = subprocess.run(["/usr/bin/java","-jar", JENKINS_CLI, "-s",ScriptInput['jenkinsserver'],"-auth", ScriptInput['auth'], "delete-node",node], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            if result.returncode == 0:
                print( "Successfully Deleted Node {0}".format(node))
                print(result.stdout)
            else:
                if result.stderr:
                    print(result.stderr)
                sys.exit(3)

def Usage():
    HelpMsg = "CommandLine Utility to add multiple nodes as jenkins slaves \n\n" \
            "Syntax:\n" \
            "\thelp:  for available options\n" \
            "\tjenkinsserver: Jenkins Server including the Port number\n" \
            "\tauth:  user account for adding slaves - USER:PASSWORD/API_KEY\n" \
            "\tnodes: jenkins slave  machine names somma separated\n" \
            "JenkinsNodeAdd.py --jenkinsserver='jenkinsserver:port' --auth='loginusername:password/api' --nodes='slavenames'\n" \
            "Example:\n" \
            "JenkinsNodeAdd.py --jenkinsserver='http://SERVERNAME:PORT' --auth='kk:XXXXXXXX' --nodes='SLAVE1,SLAVE2,SLAVE3'\n" \

    print( HelpMsg )
    sys.exit(3)


def main():
    print( " Process Input Options\n" )
    ProcessInputs()
    AddSlaves()

if __name__ == "__main__":
    main()
