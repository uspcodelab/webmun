.PHONY: dev stop docs-serve docs-build

MKDOCS ?= mkdocs

dev:
		echo "Starting dev environment"
		supabase start || npx supabase start 
		docker compose up --build 

stop:
		echo "Stopping dev environment"
		docker compose down 
		supabase stop || npx supabase stop 

docs-serve:
	$(MKDOCS) serve --config-file mkdocs.yml

docs-build:
	$(MKDOCS) build --config-file mkdocs.yml

docs-clean:
	rm -R site/
