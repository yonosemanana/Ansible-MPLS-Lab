# Test playbooks in Ansible course
This is my second course of Ansible on Pluralsight. And these repo contains test playbooks I created during the course.

## VRF configuration on Cisco IOS router
Playbook **configure_vrf.yaml** can be used to configure VRFs (route-targets, more specifically) on Cisco IOS routers in IaC manner.

### README file
This README file is also an exercise for me to use markdown language to create nice looking documentation.

For example, you can run *make* command which will do sequentially actions:
1. Use ansible-lint and pylint linters to check correctnewss of syntax and style of your code.
2. Run tests/unittest.yaml playbook which contains unit tests for custom Python filters
3. Run **configure_vrf.yaml** playbook to add necessary RTs and delete unused RTs in Cisco IOS router VRF configuration.

See below example of running the playbook.
```
✘-2 ~/Git/Ansible-MPLS-Lab [alpe-dev|✔] 
02:12 $ make -i 2> /dev/null
Start linting for Ansible playbooks and variable files and Python custom filters
find . -regex ".*.ya?ml" -not -path "./genie-lab/*" -not -path "./roles/ansible-network.network-engine/*" | xargs ansible-lint
find . -regex ".*.py" -not -path "./genie-lab/*" -not -path "./roles/ansible-network.network-engine/*" | xargs pylint
************* Module filter
plugins/filter/filter.py:8:0: R0205: Class 'FilterModule' inherits from object, can be safely removed from bases in python3 (useless-object-inheritance)
plugins/filter/filter.py:12:4: R0201: Method could be a function (no-self-use)
plugins/filter/filter.py:8:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module filter2
plugins/filter/filter2.py:40:0: C0301: Line too long (101/100) (line-too-long)
plugins/filter/filter2.py:43:0: C0301: Line too long (101/100) (line-too-long)
plugins/filter/filter2.py:9:0: R0205: Class 'FilterModule' inherits from object, can be safely removed from bases in python3 (useless-object-inheritance)
plugins/filter/filter2.py:14:4: R0201: Method could be a function (no-self-use)
plugins/filter/filter2.py:9:0: R0903: Too few public methods (1/2) (too-few-public-methods)

------------------------------------------------------------------
Your code has been rated at 8.18/10 (previous run: 8.18/10, +0.00)

End of linting
Start all unit tests
ansible-playbook tests/unittest.yaml

PLAY [PLAY - Unit tests] ********************************************************************************

TASK [Find all unit tests task files] *******************************************************************
ok: [localhost]

TASK [Get paths of the unit tests] **********************************************************************
ok: [localhost]

TASK [Run all unit tests] *******************************************************************************
included: /home/alper/Git/Ansible-MPLS-Lab/tests/tasks/test_rt_diff.yaml for localhost => (item=/home/alper/Git/Ansible-MPLS-Lab/tests/tasks/test_rt_diff.yaml)
included: /home/alper/Git/Ansible-MPLS-Lab/tests/tasks/test_ios_vrf_rt.yaml for localhost => (item=/home/alper/Git/Ansible-MPLS-Lab/tests/tasks/test_ios_vrf_rt.yaml)

TASK [Set variable - Running config] ********************************************************************
ok: [localhost]

TASK [Set variable - Intended config] *******************************************************************
ok: [localhost]

TASK [Get RT difference with custom filter 'rt_diff'] ***************************************************
ok: [localhost]

TASK [Print RT difference] ******************************************************************************
ok: [localhost] => {
    "msg": [
        {
            "add_rte": [
                "65000:1"
            ],
            "add_rti": [],
            "del_rte": [
                "65000:101"
            ],
            "del_rti": [],
            "description": "First VPN",
            "name": "VPN1",
            "rd": "65000:1"
        },
        {
            "add_rte": [
                "65000:2"
            ],
            "add_rti": [],
            "del_rte": [],
            "del_rti": [
                "65000:22"
            ],
            "description": "Second VPN",
            "name": "VPN2",
            "rd": "65000:2"
        },
        {
            "add_rte": [
                "65000:3"
            ],
            "add_rti": [
                "65000:3",
                "65000:33"
            ],
            "del_rte": [],
            "del_rti": [
                "65003:3",
                "65003:33"
            ],
            "description": "Third VPN",
            "name": "VPN3",
            "rd": "65000:3"
        }
    ]
}

TASK [ASSERT >> Ensure that three VRFs are managed by IAC] **********************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ASSERT >> Ensure VPN1 will be configured correctly] ***********************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ASSERT >> Ensure VPN2 will be configured correctly] ***********************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ASSERT >> Ensure VPN3 will be configured correctly] ***********************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Set variable - VRFs with test data] ***************************************************************
ok: [localhost]

TASK [Use custom filter being tested to parse VRF routing config] ***************************************
ok: [localhost]

TASK [Print parsed VRF data] ****************************************************************************
ok: [localhost] => {
    "msg": {
        "123": {
            "route_export": [],
            "route_import": [
                "65000:303"
            ]
        },
        "A": {
            "route_export": [
                "65000:111"
            ],
            "route_import": [
                "65000:101"
            ]
        },
        "VPN2": {
            "route_export": [
                "65000:111",
                "65000:222"
            ],
            "route_import": [
                "65000:101",
                "65000:202"
            ]
        }
    }
}

TASK [ASSERT >> Ensure VRF A parsing succeeded] *********************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ASSERT >> Ensure VRF VPN2 parcing succeeded] ******************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [ASSERT >> Ensure VRF 123 parsing succeeded] *******************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP **********************************************************************************************
localhost                  : ok=18   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

End of unit tests
Start IaC ansible-playbook to configure network devices
ansible-playbook configure_vrf.yaml -k
SSH password: 

PLAY [PLAY 1 - Configure VRFs on Cisco IOS routers based on IaC VRF variables] **************************

TASK [TASK 0 - Check if variables are set correctly] ****************************************************
ok: [R3] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [R1] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [TASK 0.1 - Check if all vrf in vrfs variable are defined correctly] *******************************
ok: [R3] => (item={'name': 'Chemical-Lab', 'description': 'Chemical Lab VRF', 'rd': '65000:2', 'route_export': ['65000:2', '65000:4'], 'route_import': ['65000:2', '65000:3']}) => {
    "ansible_loop_var": "vrf",
    "changed": false,
    "msg": "All assertions passed",
    "vrf": {
        "description": "Chemical Lab VRF",
        "name": "Chemical-Lab",
        "rd": "65000:2",
        "route_export": [
            "65000:2",
            "65000:4"
        ],
        "route_import": [
            "65000:2",
            "65000:3"
        ]
    }
}
ok: [R1] => (item={'name': 'Chemical-Lab', 'description': 'Chemical Lab VRF', 'rd': '65000:2', 'route_export': ['65000:2'], 'route_import': ['65000:2']}) => {
    "ansible_loop_var": "vrf",
    "changed": false,
    "msg": "All assertions passed",
    "vrf": {
        "description": "Chemical Lab VRF",
        "name": "Chemical-Lab",
        "rd": "65000:2",
        "route_export": [
            "65000:2"
        ],
        "route_import": [
            "65000:2"
        ]
    }
}
ok: [R1] => (item={'name': 'Police', 'description': 'Police VRF', 'rd': '65000:1', 'route_export': ['65000:1'], 'route_import': ['65000:1']}) => {
    "ansible_loop_var": "vrf",
    "changed": false,
    "msg": "All assertions passed",
    "vrf": {
        "description": "Police VRF",
        "name": "Police",
        "rd": "65000:1",
        "route_export": [
            "65000:1"
        ],
        "route_import": [
            "65000:1"
        ]
    }
}
ok: [R3] => (item={'name': 'Police', 'description': 'Police VRF', 'rd': '65000:1', 'route_export': ['65000:1'], 'route_import': ['65000:1']}) => {
    "ansible_loop_var": "vrf",
    "changed": false,
    "msg": "All assertions passed",
    "vrf": {
        "description": "Police VRF",
        "name": "Police",
        "rd": "65000:1",
        "route_export": [
            "65000:1"
        ],
        "route_import": [
            "65000:1"
        ]
    }
}
ok: [R1] => (item={'name': 'Chemical-Manager', 'description': 'Chemical Lab Manager VRF', 'rd': '65000:3', 'route_export': ['65000:3'], 'route_import': ['65000:4']}) => {
    "ansible_loop_var": "vrf",
    "changed": false,
    "msg": "All assertions passed",
    "vrf": {
        "description": "Chemical Lab Manager VRF",
        "name": "Chemical-Manager",
        "rd": "65000:3",
        "route_export": [
            "65000:3"
        ],
        "route_import": [
            "65000:4"
        ]
    }
}

TASK [TASK 1 - Get running configuration from Cisco routers] ********************************************
ok: [R3]
ok: [R1]

TASK [TASK 2 - Parse running config to get VRF config] **************************************************
ok: [R3]
ok: [R1]

TASK [TASK 3 - Check difference between intended VRF config and running config] *************************
ok: [R1]
ok: [R3]

TASK [TASK 4 - Apply VRF config difference to Cisco routers] ********************************************
changed: [R3]
changed: [R1]

RUNNING HANDLER [HANDLER 1 - Print config changes] ******************************************************
ok: [R1] => {
    "msg": {
        "banners": {},
        "changed": true,
        "commands": [
            "vrf definition Chemical-Lab",
            "rd 65000:2",
            "description Chemical Lab VRF",
            "vrf definition Police",
            "rd 65000:1",
            "description Police VRF",
            "vrf definition Chemical-Manager",
            "rd 65000:3",
            "description Chemical Lab Manager VRF"
        ],
        "failed": false,
        "updates": [
            "vrf definition Chemical-Lab",
            "rd 65000:2",
            "description Chemical Lab VRF",
            "vrf definition Police",
            "rd 65000:1",
            "description Police VRF",
            "vrf definition Chemical-Manager",
            "rd 65000:3",
            "description Chemical Lab Manager VRF"
        ],
        "warnings": [
            "To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device including the indentation"
        ]
    }
}
ok: [R3] => {
    "msg": {
        "banners": {},
        "changed": true,
        "commands": [
            "vrf definition Chemical-Lab",
            "rd 65000:2",
            "description Chemical Lab VRF",
            "vrf definition Police",
            "rd 65000:1",
            "description Police VRF"
        ],
        "failed": false,
        "updates": [
            "vrf definition Chemical-Lab",
            "rd 65000:2",
            "description Chemical Lab VRF",
            "vrf definition Police",
            "rd 65000:1",
            "description Police VRF"
        ],
        "warnings": [
            "To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device including the indentation"
        ]
    }
}

PLAY RECAP **********************************************************************************************
R1                         : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
R3                         : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

End of IaC ansible-playbooks
Run all: linting + unit test + iac playbook
✔ ~/Git/Ansible-MPLS-Lab [alpe-dev|✔] 
02:13 $ 

```
