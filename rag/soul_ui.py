#!/usr/bin/env python3
"""
Soul - Enhanced Terminal UI
A beautiful chat interface for your AI companion
"""

import os
import sys
import warnings
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.columns import Columns
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
import time

# Import your existing modules
from gemini_ai import query_anima_rag, chunk_form
from database import store_into_database
from cachesummary import store_daily_summary

class SoulUI:
    def __init__(self):
        self.console = Console()
        self.chat_history = []
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def show_header(self):
        """Display the Soul header"""
        header_text = Text()
        header_text.append("✨ ", style="bright_yellow")
        header_text.append("SOUL", style="bold bright_magenta")
        header_text.append(" ✨", style="bright_yellow")
        header_text.append("\nYour AI Companion with Memory", style="dim bright_cyan")
        
        header_panel = Panel(
            Align.center(header_text),
            border_style="bright_magenta",
            padding=(1, 2)
        )
        
        self.console.print(header_panel)
        self.console.print()
        
    def show_welcome(self):
        """Show welcome message"""
        welcome_text = Text()
        welcome_text.append("Hey! ", style="bright_cyan")
        welcome_text.append("I'm Soul, your AI friend. ", style="white")
        welcome_text.append("😊", style="bright_yellow")
        welcome_text.append("\nI'm here to chat, learn about you, and grow our friendship over time!", style="dim white")
        welcome_text.append("\nThe more we talk, the better I get to know the real you. ", style="dim cyan")
        welcome_text.append("🌱", style="bright_green")
        welcome_text.append("\n\nType 'quit' or 'exit' when you need to go.", style="dim yellow")
        
        welcome_panel = Panel(
            welcome_text,
            title="[bright_cyan]Welcome[/bright_cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print(welcome_panel)
        self.console.print()
        
    def get_user_input(self):
        """Get user input with styling"""
        self.console.print("─" * 60, style="dim white")
        user_input = Prompt.ask(
            "[bold bright_green]You[/bold bright_green]",
            console=self.console
        )
        return user_input
        
    def show_thinking(self):
        """Show thinking animation"""
        thinking_text = Text()
        thinking_text.append("🤔 ", style="bright_yellow")
        thinking_text.append("Soul is thinking...", style="dim white")
        
        with Live(thinking_text, console=self.console, refresh_per_second=4) as live:
            for i in range(6):  # Show for ~1.5 seconds
                spinner_chars = ["␋", "␙", "␹", "␸", "␼", "␴", "␦", "␧", "␇", "␏"]
                char = spinner_chars[i % len(spinner_chars)]
                thinking_text = Text()
                thinking_text.append(f"{char} ", style="bright_yellow")
                thinking_text.append("Soul is thinking...", style="dim white")
                live.update(thinking_text)
                time.sleep(0.25)
                
    def show_ai_response(self, response):
        """Display AI response with formatting"""
        self.console.print()
        
        # Create AI response text
        ai_text = Text()
        ai_text.append("🤖 ", style="bright_magenta")
        ai_text.append("Anima", style="bold bright_magenta")
        ai_text.append(":", style="bright_magenta")
        
        # Format the response
        response_panel = Panel(
            response,
            title=ai_text,
            border_style="bright_magenta",
            padding=(1, 2)
        )
        
        self.console.print(response_panel)
        self.console.print()
        
    def show_status(self, message, style="green"):
        """Show status messages"""
        status_text = Text()
        if style == "green":
            status_text.append("✅ ", style="bright_green")
        elif style == "yellow":
            status_text.append("⚠️ ", style="bright_yellow")
        elif style == "red":
            status_text.append("❌ ", style="bright_red")
            
        status_text.append(message, style=f"dim {style}")
        self.console.print(status_text)
        
    def show_memory_context(self, memories):
        """Show retrieved memories in a nice format"""
        if memories and memories != "nothing found!":
            memory_panel = Panel(
                memories,
                title="[dim]💭 Retrieved Memories[/dim]",
                border_style="dim blue",
                padding=(0, 1)
            )
            self.console.print(memory_panel)
            self.console.print()
            
    def show_error(self, error_msg):
        """Display error messages"""
        error_panel = Panel(
            f"[red]{error_msg}[/red]",
            title="[red]❌ Error[/red]",
            border_style="red"
        )
        self.console.print(error_panel)
        
    def show_goodbye(self):
        """Show goodbye message"""
        goodbye_text = Text()
        goodbye_text.append("Thanks for chatting! ", style="bright_cyan")
        goodbye_text.append("💜 ", style="bright_magenta")
        goodbye_text.append("I'll remember our conversation.", style="dim white")
        goodbye_text.append("\nSee you next time! ✨", style="bright_yellow")
        
        goodbye_panel = Panel(
            Align.center(goodbye_text),
            border_style="bright_cyan",
            padding=(1, 2)
        )
        
        self.console.print()
        self.console.print(goodbye_panel)
        
    def run_chat_session(self):
        """Main chat loop with enhanced UI"""
        try:
            while True:
                # Get user input
                user_input = self.get_user_input()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    break
                    
                # Show thinking animation
                self.show_thinking()
                
                try:
                    # Process the input (your existing logic) - no logging yet
                    results = query_anima_rag(user_input)
                    
                    # Show AI response immediately
                    self.show_ai_response(results)
                    
                    # Now do the logging and storage (after user sees response)
                    input_text = chunk_form(user_input)
                    store_into_database(input_text)
                    store_daily_summary(input_text)
                    
                    # Log the interaction after showing response
                    from output_logger import log_ai_interaction
                    log_ai_interaction(user_input, results)
                    
                    # Show success status
                    self.show_status("Added to our friendship memories", "green")
                    
                except Exception as e:
                    self.show_error(f"Sorry, something went wrong: {str(e)}")
                    
        except KeyboardInterrupt:
            pass  # Handle Ctrl+C gracefully
            
    def run(self):
        """Main application entry point"""
        self.clear_screen()
        self.show_header()
        self.show_welcome()
        
        try:
            self.run_chat_session()
        finally:
            self.show_goodbye()

def main():
    """Run the Soul UI application"""
    # Suppress deprecation warnings for cleaner UI
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    app = SoulUI()
    app.run()

if __name__ == "__main__":
    main()
