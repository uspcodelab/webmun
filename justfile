set default-list := true

MKDOCS := "mkdocs"

# start the dev environment
start-dev:
	echo "Starting dev environment"
	supabase start || npx supabase start 
	docker compose up --watch

# stop dev environment
stop-dev:
	echo "Stopping dev environment"
	docker compose down 
	supabase stop || npx supabase stop 

# stop and clean containers, images, and volumes
clean-dev:
	docker compose down -v --rmi all --remove-orphans
	supabase stop --no-backup

# serve documentation using mkdocs
docs-serve:
	{{MKDOCS}} serve --config-file mkdocs.yml

# build documentation using mkdocs
docs-build:
	{{MKDOCS}} build --config-file mkdocs.yml

# cleanup documentation
docs-clean:
	rm -rf site/
