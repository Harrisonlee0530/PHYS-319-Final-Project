#include <msp430f5529.h>
#include<stdio.h>

# define TXD  BIT4              // TXD on P4.4
# define RXD  BIT5              // RXD on P4.5
# define LED1 BIT0              // P1.0 LED
# define LED2 BIT7              // P4.7 LED
# define INPUT BIT0             // input from microphone  on P6.0

unsigned int TXByte;

int main(void) {
    WDTCTL = WDTPW + WDTHOLD;   // stop watchdog timer

    // configure ADC
    ADC12CTL0 = ADC12SHT02 + ADC12ON;   // Sampling time, ADC12 on
    ADC12CTL1 = ADC12SHP;               // sampling timer
    ADC12CTL0 |= ADC12ENC;              // ADC enable
    P6SEL |= 0x01;                      // P6.0 allow ADC on pin 6.0

    ADC12MCTL0 = ADC12INCH_0;
          //selects which input results are
          //stored in memory ADC12MEM0. Input
          //one is selected on reset so this line is not needed
          //Must be written before enabling conversions

    ADC12CTL0 |= ADC12ENC;              // ADC enable

    /* Configure hardware UART */
    UCA1CTL1 = UCSWRST;         // Recommended to place USCI in reset first
    P4SEL |= BIT4 + BIT5;
    UCA1CTL1 |= UCSSEL_2;       // Use SMCLK
    UCA1BR0 = 109;              // Set baud rate to 9600 with 1.048MHz clock (Data Sheet 36.3.13)
    UCA1BR1 = 0;                // Set baud rate to 9600 with 1.048MHz clock
    UCA1MCTL = UCBRS_2;         // Modulation UCBRSx = 2
    UCA1CTL1 &= ~UCSWRST;       // Initialize USCI state machine
    /* if we were going to receive, we would also:
        IE2 |= UCA1RXIE; // Enable USCI_A1 RX interrupt
    */

    // output pin to computer
    P4DIR |= TXD;
    P4OUT |= TXD;

    // LED for function testing
    P1DIR |= LED1;
    P1OUT |= LED1;

    P4DIR |= LED2;
    P4OUT &= ~LED2;

    while (1) {
        ADC12CTL0 |= ADC12SC;           // Start sampling
        while (ADC12CTL1 & ADC12BUSY);  // while bit ADC12BUSY in register ADC12CTL1 is high wait

        while (! (UCA1IFG & UCTXIFG)); // wait for TX buffer to be ready for new data

        TXByte = ADC12MEM0/10;     // input voltage proportional to the volume of the audio signal
        UCA1TXBUF = TXByte;     // Transmit TXByte;

        P1OUT ^= LED1;          // toggle LED1
        P4OUT ^= LED2;          // toggle LED2

        _delay_cycles(10000);  // wait for 20 milliseconds before repeating
    }
}
