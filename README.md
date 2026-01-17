AI-powered all-in-one travel planning dashboard using Llama-3 and Streamlit. Plan trips, track budgets, build itineraries, pack smarter, and chat with AI travel assistant.

✨ Features:-

     1.🗺️ Smart Planner:	AI generates personalized itineraries based on destination, budget, interests, and trip type
     2.📅 Day-by-Day Itinerary:	Organize morning, afternoon, and evening activities with easy editing
     3.💰 Budget Tracker:	Real-time expense tracking with category breakdowns and remaining budget alerts
     4.🎒 Packing Checklist:	Smart packing lists with progress tracking and item management
     5.❤️ Wishlist:	Save favorite destinations and attractions for future trips
     6.💬 AI Chatbot:	Instant travel advice powered by Llama-3 (best restaurants, local tips, etc.)
     7.📊 Multi-Trip Management:	Plan and manage multiple trips simultaneously


✨Prerequisites:-

      Python 3.11 or higher
      pip (Python package manager)
      HuggingFace Account (free)
      Streamlit
      VScode/Googlecolab

How to get HF_TOKEN:-

  1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
  2. Click "New Token" → "User" (read)
  3. Copy and paste in `secrets.toml`

[Note: User has to input their own HF_TOKEN in the secrets file and change the code to extract it]

🎨 How to Use:-

Plan Itinerary
1. Go to "📅 Itinerary" tab
2. Expand each day
3. Add morning/afternoon/evening activities
4. Click "**Save Day**"

Track Budget
1. Go to "💰 Budget" tab
2. Select category (Accommodation, Food, etc.)
3. Enter amount and description
4. Click "**➕ Add Expense**"
5. View real-time budget breakdown

Add to Wishlist
1. Go to "❤️ Favorites" tab
2. Enter favorite destination/place
3. Click "**❤️ Add**"

Pack Smart
1. Go to "🎒 Packing" tab
2. Add items (Passport, Sunscreen, etc.)
3. Check off as you pack
4. View packing progress

Chat with AI
1. Go to "💬 Travel AI" tab
2. Ask questions: "Best restaurants in Paris?"
3. Click "**🤖 Get AI Response**"


Troubleshooting:-

| `StreamlitValueBelowMinError` | Budget must be ≥ $100 |
| `HF_TOKEN not found` | Check `.streamlit/secrets.toml` exists |
| `Port 8501 already in use` | `streamlit run app.py --server.port 8502` |
| `AI repeating responses` | Check API token is valid, restart app |

License:-

MIT License - Feel free to use, modify, and distribute!

Copyright (c) 2026 [Parnabha Sarkar]

Permission is hereby granted, free of charge, to any person obtaining a copy...

⭐ **Show Your Support**

If this project helped you plan your trips, please **star this repo**! ⭐