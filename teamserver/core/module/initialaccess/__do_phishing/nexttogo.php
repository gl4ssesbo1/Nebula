
    <?php
    
        $url = "https://cloud.digitalocean.com/";

        ob_start();
        header('Location: '.$url);
        ob_end_flush();
        //die();
    ?>
        