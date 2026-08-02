import { supabase } from "@/lib/supabaseClient"

  export async function apiFetch(
    path: string,
    init: RequestInit = {},
  ): Promise<Response> {
    const { data: { session } } = await supabase.auth.getSession()

    if (!session) {
      throw new Error("Authentication required")
    }

    return fetch(`${import.meta.env.VITE_API_URL}${path}`, {
      ...init,
      headers: {
        ...init.headers,
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
    })
  }
