import Navbar from "@/components/homepage/navbar"
import Footer from "@/components/homepage/footer"

export default function Home() {
    return (
        <div className="flex h-screen w-screen flex-col">
            <Navbar />
            <h1>Home Page</h1>
            <Footer />
        </div>
    )
}