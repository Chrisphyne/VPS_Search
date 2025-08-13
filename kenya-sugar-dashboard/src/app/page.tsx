import ChatInterface from '@/components/ChatInterface'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-green-50 to-orange-50 p-4">
      <div className="max-w-3xl mx-auto">
        <ChatInterface />
      </div>
    </main>
  )
}
