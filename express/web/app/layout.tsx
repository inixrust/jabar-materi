import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import '../styles/tokens.css';
import './globals.css';

export const metadata: Metadata = {
  title: 'Catatan Tim',
  description: 'Kerangka proyek pelatihan Developing dengan AI',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
