import base64
import os
import sys
import time

import boto3
import requests
from termcolor import colored

def checkBucket(bucketname):
    statuscode = requests.get(f"https://{bucketname}.s3.amazonaws.com").status_code
    if statuscode == 200 or statuscode == 403:
        return True
    return False

def getparticlelist(profile, bucket_name, particles):
    try:
        s3Client = boto3.Session(profile_name=profile).client("s3")
        bucketObjectsReq = s3Client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in bucketObjectsReq:
            bucketObjects = bucketObjectsReq['Contents']
            for key in bucketObjects:
                if key['key'][-1] == "/":
                    if not key['key'][-1] in particles:
                        particles.append(key['key'][-1])
    except:
        print(
            colored(
                f"[*] Error: {sys.exc_info()[1]}", "red"
            )
        )
def getsendcommand(bucket_name, particle_name, command_key, output_key, command, s3Client, kmskeyid, particles):
    testparticle = 0
    try:
        #s3Client = boto3.Session(profile_name=profile).client("s3")
        bucketObjectsReq = s3Client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in bucketObjectsReq:
            bucketObjects = bucketObjectsReq['Contents']
            objcheck = 0
            for object in bucketObjects:
                if object['Key'] == f"{particle_name}/{output_key}":
                    objcheck = 1
                    try:
                        print(s3Client.get_object(
                            Bucket=bucket_name,
                            Key=f"{particle_name}/{output_key}",
                            # SSEKMSKeyId=kmskeyid,
                            # ServerSideEncryption ='aws:kms'
                        )['Body'].read().decode())
                    except:
                        pass
                    s3Client.delete_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{output_key}",
                        # SSEKMSKeyId=kmskeyid,
                        # ServerSideEncryption ='aws:kms'
                    )

                    s3Client.delete_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{command_key}",
                        #SSEKMSKeyId=kmskeyid,
                        #ServerSideEncryption ='aws:kms'
                    )

                    with open("/tmp/command", "w") as cf:
                        cf.write(command)
                        cf.close()

                    with open("/tmp/command", "rb") as f:
                        s3Client.put_object(
                            Bucket=bucket_name,
                            Key=f"{particle_name}/{command_key}",
                            Body=base64.b64encode(f.read()),
                            SSEKMSKeyId = kmskeyid,
                            ServerSideEncryption ='aws:kms',
                            ContentType="text/plain"
                        )

                    print(
                        colored(
                            f"[*] Uploaded command to bucket", "green"
                        )
                    )
                    os.remove("/tmp/command")

                    while True:
                        try:
                            print(s3Client.get_object(
                                Bucket=bucket_name,
                                Key=f"{particle_name}/{output_key}",
                                # SSEKMSKeyId=kmskeyid,
                                # ServerSideEncryption ='aws:kms'
                            )['Body'].read().decode())

                            s3Client.delete_object(
                                Bucket=bucket_name,
                                Key=f"{particle_name}/{output_key}",
                                # SSEKMSKeyId=kmskeyid,
                                # ServerSideEncryption ='aws:kms'
                            )

                            s3Client.delete_object(
                                Bucket=bucket_name,
                                Key=f"{particle_name}/{command_key}",
                                # SSEKMSKeyId=kmskeyid,
                                # ServerSideEncryption ='aws:kms'
                            )
                            break
                        except:
                            time.sleep(5)
                            testparticle += 5
                            if testparticle == 30:
                                deleteparticle(s3Client, particle_name, bucket_name, command_key, output_key, particles)
                                particle_name = ""
                                break
                            pass

            if objcheck == 0:
                with open("/tmp/command", "w") as cf:
                    cf.write(command)
                    cf.close()

                with open("/tmp/command", "rb") as f:

                    s3Client.put_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{command_key}",
                        Body=base64.b64encode(f.read()),
                        SSEKMSKeyId=kmskeyid,
                        ServerSideEncryption ='aws:kms',
                        ContentType="text/plain"
                        #ContentEncoding="text/plain"
                    )

                print(
                    colored(
                        f"[*] Uploaded command to bucket", "green"
                    )
                )
                os.remove("/tmp/command")
                while True:
                    try:
                        print(s3Client.get_object(
                            Bucket=bucket_name,
                            Key=f"{particle_name}/{output_key}",
                            #SSEKMSKeyId=kmskeyid,
                            #ServerSideEncryption ='aws:kms'
                        )['Body'].read().decode())

                        s3Client.delete_object(
                            Bucket=bucket_name,
                            Key=f"{particle_name}/{output_key}",
                            # SSEKMSKeyId=kmskeyid,
                            # ServerSideEncryption ='aws:kms'
                        )

                        s3Client.delete_object(
                            Bucket=bucket_name,
                            Key=f"{particle_name}/{command_key}",
                            # SSEKMSKeyId=kmskeyid,
                            # ServerSideEncryption ='aws:kms'
                        )

                        break
                    except:
                        time.sleep(5)
                        testparticle += 5
                        if testparticle == 30:
                            deleteparticle(s3Client, particle_name, bucket_name, command_key, output_key, particles)
                            particle_name = ""
                            break
                        pass

        else:
            with open("/tmp/command", "w") as cf:
                cf.write(command)
                cf.close()

            with open("/tmp/command", "rb") as f:
                s3Client.put_object(
                    Bucket=bucket_name,
                    Key=f"{particle_name}/{command_key}",
                    Body=base64.b64encode(f.read()),
                    SSEKMSKeyId=kmskeyid,
                    ServerSideEncryption ='aws:kms',
                    ContentType="text/plain"
                )

            print(
                colored(
                    f"[*] Uploaded command to bucket", "green"
                )
            )
            os.remove("/tmp/command")
            while True:
                try:
                    print(s3Client.get_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{output_key}",
                        # SSEKMSKeyId=kmskeyid,
                        # ServerSideEncryption ='aws:kms'
                    )['Body'].read().decode())

                    s3Client.delete_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{output_key}",
                        # SSEKMSKeyId=kmskeyid,
                        # ServerSideEncryption ='aws:kms'
                    )

                    s3Client.delete_object(
                        Bucket=bucket_name,
                        Key=f"{particle_name}/{command_key}",
                        # SSEKMSKeyId=kmskeyid,
                        # ServerSideEncryption ='aws:kms'
                    )

                    break
                except:
                    time.sleep(5)
                    testparticle += 5
                    if testparticle == 30:
                        deleteparticle(s3Client, particle_name, bucket_name, command_key, output_key, particles)
                        particle_name = ""
                        break
                    pass


    except:
        print(
            colored(
                f"[*] Error: {sys.exc_info()[1]}", "red"
            )
        )

def deleteparticle(s3Client, particle_name, bucket_name, commandfile, outputfile, particles):
    print(colored(
        "The particle seems down. Deleting the bucket dir", "yellow"
    ))

    try:
        s3Client.delete_object(
            Bucket=bucket_name,
            Key=f"{particle_name}/{commandfile}"
        )
    except:
        pass
    try:
        s3Client.delete_object(
            Bucket=bucket_name,
            Key=f"{particle_name}/{outputfile}"
        )
    except:
        pass

    try:
        s3Client.delete_object(
            Bucket=bucket_name,
            Key=f"{particle_name}/"
        )
    except:
        pass

    for particlelist in particles:
        if particlelist['particle_key_name'] == particle_name:
            del (particles[particles.index(particlelist)])

    print(
        colored(
        "Particle Deleted", "green"
        )
    )

