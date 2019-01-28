# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
import papermill as pm
from tests.notebooks_common import OUTPUT_NOTEBOOK, KERNEL_NAME


TOL = 0.05

@pytest.mark.smoke
def test_sar_single_node_smoke(notebooks):
    notebook_path = notebooks["sar_single_node"]
    pm.execute_notebook(notebook_path, OUTPUT_NOTEBOOK, kernel_name=KERNEL_NAME)
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE="100k"),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    assert results["map"] == pytest.approx(0.105815262, TOL)
    assert results["ndcg"] == pytest.approx(0.373197255, TOL)
    assert results["precision"] == pytest.approx(0.326617179, TOL)
    assert results["recall"] == pytest.approx(0.175956743, TOL)


@pytest.mark.smoke
def test_baseline_deep_dive_smoke(notebooks):
    notebook_path = notebooks["baseline_deep_dive"]
    pm.execute_notebook(notebook_path, OUTPUT_NOTEBOOK, kernel_name=KERNEL_NAME)
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE="100k"),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    assert results["rmse"] == pytest.approx(1.054252, TOL)
    assert results["mae"] == pytest.approx(0.846033, TOL)
    assert results["rsquared"] == pytest.approx(0.136435, TOL)
    assert results["exp_var"] == pytest.approx(0.136446, TOL)
    assert results["map"] == pytest.approx(0.052850, TOL)
    assert results["ndcg"] == pytest.approx(0.248061, TOL)
    assert results["precision"] == pytest.approx(0.223754, TOL)
    assert results["recall"] == pytest.approx(0.108826, TOL)

@pytest.mark.smoke
def test_fastai(notebooks):
    notebook_path = notebooks["fastai"]
    pm.execute_notebook(notebook_path, OUTPUT_NOTEBOOK, kernel_name=KERNEL_NAME)
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE="100k"),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    assert results["rmse"] == pytest.approx(0.912115, TOL)
    assert results["mae"] == pytest.approx(0.723051, TOL)
    assert results["rsquared"] == pytest.approx(0.356302, TOL)
    assert results["exp_var"] == pytest.approx(0.357081, TOL)
    assert results["map"] == pytest.approx(0.021485, TOL)
    assert results["ndcg"] == pytest.approx(0.137494, TOL)
    assert results["precision"] == pytest.approx(0.124284, TOL)
    assert results["recall"] == pytest.approx(0.045587, TOL)

@pytest.mark.smoke
def test_adb_setup(notebooks):
    notebook_path = notebooks["adb_setup"]
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(path_to_recommenders_repo_root="./", 
            record_for_tests=True, 
            TOKEN="",
            autotermination_minutes=15
        )
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    ## 200 if the cluster is avail, 400 if the cluster is off
    assert results["lib_install_code"] == 200 or results["lib_install_code"] == 400
    ## this should always be able to be 200
    assert results["lib_status_code"] == 200 
    assert results["nb_upload_code"] == 200 or (results["nb_upload_code"] == 400 and results["nb_upload_json"].error_code == "RESOURCE_ALREADY_EXISTS")
