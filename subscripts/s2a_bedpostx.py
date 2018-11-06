#!/usr/bin/env python3
from subscripts.config import executor_labels
from parsl.app.app import python_app

@python_app(executors=executor_labels)
def s2a_bedpostx(sdir, cores_per_task, stdout, container, checksum, use_gpu):
    import time
    from subscripts.utilities import run,smart_mkdir,smart_remove,write,record_start,record_apptime,record_finish
    from os.path import exists,join
    from shutil import copyfile,rmtree
    record_start(sdir, stdout, 's2a')
    start_time = time.time()
    bedpostx = join(sdir,"bedpostx_b1000")
    bedpostxResults = join(sdir,"bedpostx_b1000.bedpostX")
    th1 = join(bedpostxResults, "merged_th1samples")
    ph1 = join(bedpostxResults, "merged_ph1samples")
    th2 = join(bedpostxResults, "merged_th2samples")
    ph2 = join(bedpostxResults, "merged_ph2samples")
    dyads1 = join(bedpostxResults, "dyads1")
    dyads2 = join(bedpostxResults, "dyads2")
    brain_mask = join(bedpostxResults, "nodif_brain_mask")
    if exists(bedpostxResults):
        rmtree(bedpostxResults)
    smart_mkdir(bedpostx)
    smart_mkdir(bedpostxResults)
    copyfile(join(sdir,"data_eddy.nii.gz"),join(bedpostx,"data.nii.gz"))
    copyfile(join(sdir,"data_bet_mask.nii.gz"),join(bedpostx,"nodif_brain_mask.nii.gz"))
    copyfile(join(sdir,"bvals"),join(bedpostx,"bvals"))
    copyfile(join(sdir,"bvecs"),join(bedpostx,"bvecs"))

    if use_gpu:
        write(stdout, "Running Bedpostx without GPU")
        run("bedpostx_gpu {} -NJOBS 4".format(bedpostx), stdout, container)
    else:
        write(stdout, "Running Bedpostx without GPU")
        run("bedpostx {}".format(bedpostx), stdout, container)
    run("make_dyadic_vectors {} {} {} {}".format(th1,ph1,brain_mask,dyads1), stdout, container)
    run("make_dyadic_vectors {} {} {} {}".format(th2,ph2,brain_mask,dyads2), stdout, container)
    record_apptime(sdir, start_time, 's2a')
    record_finish(sdir, stdout, cores_per_task, 's2a')

def create_job(sdir, cores_per_task, stdout, container, checksum, use_gpu):
    return s2a_bedpostx(sdir, cores_per_task, stdout, container, checksum, use_gpu)