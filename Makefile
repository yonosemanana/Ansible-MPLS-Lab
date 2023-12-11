.DEFAULT_GOAL := run

.PHONY: run
run: lint unittest iac
	@echo "Run all: linting + unit test + iac playbook"

.PHONY: lint
lint:
	@echo "Start linting for Ansible playbooks and variable files and Python custom filters"
	find . -regex ".*.ya?ml" -not -path "./genie-lab/*" -not -path "./roles/ansible-network.network-engine/*" | xargs ansible-lint
	find . -regex ".*.py" -not -path "./genie-lab/*" -not -path "./roles/ansible-network.network-engine/*" | xargs pylint
	@echo "End of linting"

.PHONY: unittest
unittest:
	@echo "Start all unit tests"
	ansible-playbook tests/unittest.yaml
	@echo "End of unit tests"

.PHONY: iac
iac:
	@echo "Start IaC ansible-playbook to configure network devices"
	ansible-playbook configure_vrf.yaml -k
	@echo "End of IaC ansible-playbooks"
