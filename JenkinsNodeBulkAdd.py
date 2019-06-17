#!/usr/bin/python3.6

### Modules Imports
import sys, getopt
import subprocess
import os
import time

### Global Variables 
SSH_PORT = "22"
JENKINS_CLI = "/usr/bin/jenkins-cli.jar"
SLAVE_CONFIG = ''


ScriptInput = {}

def ProcessInputs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:s:a:n:l:u:r:e:c:", [ "help", "jenkinsserver=", "auth=", "nodes=", "label=", "username=", "slavehome=", "executors=", "slavecreds=" ]) 
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
        elif opt in ('-l', '--label'):
            ScriptInput['label'] = arg
        elif opt in ('-u', '--username'):
            ScriptInput['username'] = arg
        elif opt in ('-r', '--slavehome'):
            ScriptInput['slavehome'] = arg
        elif opt in ('-c', '--slavecreds'):
            ScriptInput['slavecreds'] = arg
        elif opt in ('-e', '--executors'):
            ScriptInput['executors'] = arg
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
        
    if 'label' not in ScriptInput:
        print( "labels option is mandatory\n" )
        Usage()
    
    if 'username' not in ScriptInput:
        print( "username option is mandatory\n" )
        Usage()
    
    if 'slavehome' not in ScriptInput:
        print( "slavehome option is mandatory\n" )
        Usage()
    
    if 'executors' not in ScriptInput:
        print( "executors option is mandatory\n" )
        Usage()

    if 'slavecreds' not in ScriptInput:
        print( "slavecreds option is mandatory\n" )
        Usage()
def AddSlaves():
    print( "Adding Slaves to Jenkins \n" )

    Nodes = ScriptInput['nodes'].split(",")

    for node in Nodes:
        print( "Adding node: {0}".format(node))
        SLAVE_CONFIG = "<slave>" \
        "<name>{0}</name>" \
        "<description></description>" \
        "<remoteFS>{1}</remoteFS>" \
        "<numExecutors>{2}</numExecutors>" \
        "<mode>EXCLUSIVE</mode>" \
        "<retentionStrategy class=\"hudson.slaves.RetentionStrategy$Always\"/> " \
        "<launcher class=\"hudson.plugins.sshslaves.SSHLauncher\" plugin=\"ssh-slaves@1.28\">" \
        "<host>{3}</host>" \
        "<port>{4}</port>" \
        "<credentialsId>{5}</credentialsId>" \
        "<javaPath>/usr/software/java/jdk1.8.0_162/bin/java</javaPath>" \
        "<launchTimeoutSeconds>210</launchTimeoutSeconds>" \
        "<maxNumRetries>10</maxNumRetries>" \
        "<retryWaitTime>15</retryWaitTime>" \
        "<sshHostKeyVerificationStrategy class=\"hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy\"/>" \
        "<tcpNoDelay>true</tcpNoDelay>" \
        "</launcher>" \
        "<label>{6}</label>" \
        "<nodeProperties/> </slave>".format(node,ScriptInput['slavehome'], ScriptInput['executors'], node, SSH_PORT,ScriptInput['slavecreds'] , ScriptInput['label'])

        #JENKINS_CMD = "/usr/bin/java -jar {0} -s {1} create-node {2} {3}".format( JENKINS_CLI, ScriptInput['jenkinsserver'], node,SLAVE_CONFIG ) 
        #JENKINS_CMD = "/usr/bin/java -jar {0} -s {1} get-node {2}".format( JENKINS_CLI, ScriptInput['jenkinsserver'], node ) 
        print(SLAVE_CONFIG) 

###### Create Slaveconfig file 
        epoch_time = int(time.time())
        myslaveconfigfile = "/tmp/slaveconfig{0}.xml".format(epoch_time)

        print( "Creating Slave Config file {0}".format(myslaveconfigfile) )

        try:
            myconfig = open( myslaveconfigfile, "w+" )
            myconfig.write(SLAVE_CONFIG)
            myconfig.close()
            print(" Slave Configuration creation for node '{0}' is successful!".format(myslaveconfigfile))
        except IOError:
            print( "Could not open file '{0}'".format(myslaveconfigfile))
            sys.exit(3)

        try:
            myinput = open(myslaveconfigfile)
            print( " Running create-node command to add slave\n" )
            result = subprocess.run(["/usr/bin/java","-jar", JENKINS_CLI, "-s",ScriptInput['jenkinsserver'],"-auth", ScriptInput['auth'], "create-node",node], stdin=myinput, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            if result.returncode == 0:
                print( "Successfully Add Node {0} as slave".format(node))
                print(result.stdout)
            else:
                if result.stderr:
                    print(result.stderr)
                sys.exit(3)
            myinput.close()
            print( "Unlinking the temperorary config file" )
            os.unlink(myslaveconfigfile)

        except IOError:
            print( "Could not open file '{0}".format(myslaveconfigfile))
            sys.exit(3)

def Usage():
    HelpMsg = "CommandLine Utility to add multiple nodes as jenkins slaves \n\n" \
            "Syntax:\n" \
            "\thelp:  for available options\n" \
            "\tjenkinsserver: Jenkins Server including the Port number\n" \
            "\tauth:  user account for adding slaves - USER:PASSWORD/API_KEY\n" \
            "\tnodes: jenkins slave  machine names somma separated\n" \
            "\tlabel: slave group name\n" \
            "\tusername: default user for the slave machine\n\n" \
            "slavecreds: credential id of default slave user" \
            "JenkinsNodeAdd.py --jenkinsserver='jenkinsserver:port' --auth='loginusername:password/api' --nodes='slavenames' --label='label expression' --username='default slave username' --executors='number of executors' --slavehome='Remote root Directory' --slavecreds='credentials id' \n" \
            "Example:\n" \
            "JenkinsNodeAdd.py --jenkinsserver='http://SERVERNAME:PORT' --auth='kkk:XXXXXXXX' --nodes='SLAVE1,SLAVE2,SLAVE3,SLAVE4' --label='bldservers' --username='testuser' --executors='10' --slavehome='/tmp'  --slavecreds='CCCCCCCC'\n" \

    print( HelpMsg )
    sys.exit(3)


def main():
    print( " Process Input Options\n" )
    ProcessInputs()
    AddSlaves()

if __name__ == "__main__":
    main()
