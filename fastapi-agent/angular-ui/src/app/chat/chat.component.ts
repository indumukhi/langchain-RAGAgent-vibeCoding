import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ChatService, ChatMessage } from '../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent {
  @ViewChild('messageList') private messageList!: ElementRef;

  messages: ChatMessage[] = [];
  userInput = '';
  loading = false;
  errorMessage = '';

  constructor(private chatService: ChatService) {}

  send(): void {
    const question = this.userInput.trim();
    if (!question || this.loading) return;

    this.messages.push({ role: 'user', text: question, timestamp: new Date() });
    this.userInput = '';
    this.loading = true;
    this.errorMessage = '';

    this.chatService.ask(question).subscribe({
      next: (res) => {
        this.messages.push({ role: 'assistant', text: res.answer, timestamp: new Date() });
        this.loading = false;
        this.scrollToBottom();
      },
      error: (err) => {
        this.errorMessage = 'Something went wrong. Please try again.';
        this.loading = false;
        console.error(err);
      },
    });

    this.scrollToBottom();
  }

  onEnter(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.messageList) {
        this.messageList.nativeElement.scrollTop = this.messageList.nativeElement.scrollHeight;
      }
    }, 50);
  }
}
