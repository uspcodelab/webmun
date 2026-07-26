.PHONY: dev stop 

dev:
		echo "Starting dev environment"
		supabase start || npx supabase start 
		docker compose up --build 

stop:
		echo "Stopping dev environment"
		docker compose down 
		supabase stop || npx supabase stop 


