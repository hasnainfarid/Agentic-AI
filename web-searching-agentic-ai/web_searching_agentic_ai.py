#!/usr/bin/env python3
"""
Web-Searching Agentic AI
A powerful ReAct agent with GUI, real-time web search, and intelligent tool usage
Author: Hasnain Fareed (2025)
License: MIT
"""

import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# Set API keys from environment variables
# Get your API keys from:
# Groq: https://console.groq.com/keys
# Tavily: https://tavily.com/
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY environment variable")
if not TAVILY_API_KEY:
    raise ValueError("Please set TAVILY_API_KEY environment variable")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

class WebSearchingAgenticAI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Web-Searching Agentic AI")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize agent as None first
        self.agent = None
        
        # Create GUI first
        self.create_widgets()
        
        # Initialize agent in a separate thread to avoid blocking GUI
        threading.Thread(target=self.setup_agent, daemon=True).start()
        
    def setup_agent(self):
        """Initialize the ReAct agent"""
        try:
            # Initialize Tavily search tool
            tavily_search = TavilySearchResults()
            
            # Define tools
            tools = [
                Tool(
                    name="Calculator",
                    description="Useful for math calculations. Input should be a math expression like '2+2' or '10*5'",
                    func=self.calculator
                ),
                Tool(
                    name="Weather",
                    description="Useful for weather information. Input should be a city name",
                    func=self.weather_tool
                ),
                tavily_search
            ]
            
            # Initialize Groq LLM
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0,
                groq_api_key=os.environ["GROQ_API_KEY"]
            )
            
            # Initialize ReAct agent
            self.agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent="zero-shot-react-description",
                verbose=False,  # We'll handle verbose output ourselves
                handle_parsing_errors=True,
                max_iterations=3
            )
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.log_message("✅ Agent initialized successfully!", "success"))
            
        except Exception as e:
            # Update GUI in main thread
            self.root.after(0, lambda: self.log_message(f"❌ Error initializing agent: {e}", "error"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to initialize agent: {e}"))
    
    def calculator(self, input_str):
        """Simple calculator tool"""
        try:
            safe_chars = "0123456789+-*/(). "
            cleaned = ''.join(c for c in input_str if c in safe_chars)
            result = eval(cleaned)
            return str(result)
        except:
            return "Error: Could not calculate that expression"
    
    def weather_tool(self, input_str):
        """Mock weather tool"""
        return f"Weather in {input_str}: Sunny, 25°C"
    
    def create_widgets(self):
        """Create the GUI widgets"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🤖 Web-Searching Agentic AI", 
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(input_frame, text="Your Question:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        self.input_text = tk.Text(input_frame, height=3, font=('Arial', 11))
        self.input_text.pack(fill='x', pady=(5, 10))
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.send_button = tk.Button(
            button_frame,
            text="🚀 Send Query",
            command=self.send_query,
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.send_button.pack(side='left')
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            font=('Arial', 11),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.clear_button.pack(side='left', padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            button_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side='right', padx=(10, 0))
        
        # Main content area
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # ReAct Steps tab
        self.steps_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.steps_frame, text="🧠 ReAct Steps")
        
        self.steps_text = scrolledtext.ScrolledText(
            self.steps_frame,
            font=('Consolas', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white',
            wrap=tk.WORD
        )
        self.steps_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Conversation tab
        self.conversation_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.conversation_frame, text="💬 Conversation")
        
        self.conversation_text = scrolledtext.ScrolledText(
            self.conversation_frame,
            font=('Arial', 11),
            bg='#ffffff',
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.conversation_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        self.status_frame.pack(fill='x', padx=10, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to assist you!",
            font=('Arial', 9),
            fg='white',
            bg='#34495e'
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Bind Enter key to send query
        self.input_text.bind('<Return>', lambda e: self.send_query())
        
    def log_message(self, message, msg_type="info"):
        """Log a message with timestamp and color coding"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        colors = {
            "info": "#3498db",
            "success": "#27ae60", 
            "error": "#e74c3c",
            "warning": "#f39c12",
            "thinking": "#9b59b6",
            "action": "#e67e22",
            "observation": "#16a085"
        }
        
        color = colors.get(msg_type, "#2c3e50")
        
        # Add to steps text
        self.steps_text.config(state='normal')
        self.steps_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.steps_text.insert(tk.END, f"{message}\n", msg_type)
        self.steps_text.config(state='disabled')
        self.steps_text.see(tk.END)
        
        # Configure tags for colors
        self.steps_text.tag_configure("timestamp", foreground="#95a5a6")
        self.steps_text.tag_configure(msg_type, foreground=color, font=('Consolas', 10, 'bold'))
        
    def send_query(self):
        """Send query to the agent"""
        query = self.input_text.get("1.0", tk.END).strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter a question!")
            return
            
        if not self.agent:
            messagebox.showerror("Error", "Agent not initialized!")
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add to conversation
        self.add_to_conversation(f"👤 You: {query}")
        
        # Start processing in a separate thread
        self.progress.start()
        self.send_button.config(state='disabled', text="⏳ Processing...")
        self.status_label.config(text="Processing your query...")
        
        thread = threading.Thread(target=self.process_query, args=(query,))
        thread.daemon = True
        thread.start()
        
    def process_query(self, query):
        """Process the query with the agent"""
        try:
            self.log_message(f"🤔 Received query: {query}", "thinking")
            
            # Capture the agent's verbose output
            import io
            import sys
            
            # Create a custom output capture
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            try:
                # Run the agent using invoke instead of deprecated run
                response = self.agent.invoke({"input": query})
                response_text = response.get("output", str(response))
                
                # Get the captured output
                agent_output = captured_output.getvalue()
                
                # Debug: Log the raw response
                self.root.after(0, lambda: self.log_message(f"🔍 Raw response: {response_text[:100]}...", "info"))
                
                # Parse and display the ReAct steps
                self.parse_react_steps(agent_output)
                
                # Add final response to conversation (in main thread)
                self.root.after(0, lambda: self.add_to_conversation(f"🤖 Agent: {response_text}"))
                
                self.root.after(0, lambda: self.log_message("✅ Query processed successfully!", "success"))
                
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Error processing query: {e}", "error"))
            self.root.after(0, lambda: self.add_to_conversation(f"❌ Error: {e}"))
            
        finally:
            # Re-enable UI
            self.root.after(0, self.reset_ui)
    
    def parse_react_steps(self, output):
        """Parse and display ReAct steps"""
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Thought:'):
                self.root.after(0, lambda l=line: self.log_message(f"🧠 {l}", "thinking"))
            elif line.startswith('Action:'):
                self.root.after(0, lambda l=line: self.log_message(f"⚡ {l}", "action"))
            elif line.startswith('Action Input:'):
                self.root.after(0, lambda l=line: self.log_message(f"📝 {l}", "action"))
            elif line.startswith('Observation:'):
                self.root.after(0, lambda l=line: self.log_message(f"👁️ {l}", "observation"))
            elif line.startswith('Final Answer:'):
                self.root.after(0, lambda l=line: self.log_message(f"✅ {l}", "success"))
    
    def add_to_conversation(self, message):
        """Add message to conversation tab"""
        self.conversation_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_text.insert(tk.END, f"[{timestamp}] {message}\n\n")
        self.conversation_text.config(state='disabled')
        self.conversation_text.see(tk.END)
    
    def reset_ui(self):
        """Reset UI elements"""
        self.progress.stop()
        self.send_button.config(state='normal', text="🚀 Send Query")
        self.status_label.config(text="Ready to assist you!")
    
    def clear_all(self):
        """Clear all text areas"""
        self.steps_text.config(state='normal')
        self.steps_text.delete("1.0", tk.END)
        self.steps_text.config(state='disabled')
        
        self.conversation_text.config(state='normal')
        self.conversation_text.delete("1.0", tk.END)
        self.conversation_text.config(state='disabled')
        
        self.input_text.delete("1.0", tk.END)
        self.log_message("🗑️ Cleared all content", "info")

def main():
    root = tk.Tk()
    app = WebSearchingAgenticAI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
