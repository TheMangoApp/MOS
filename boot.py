import boot_lib
status = "STARTING"
while status != "STOPPED":
    status = boot_lib.ota()