import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatAddress(address: string): string {
  if (!address) return '';
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

export function formatEther(value: string | number): string {
  return parseFloat(value.toString()).toFixed(4);
}

export function getEtherscanUrl(txHash: string): string {
  return `https://sepolia.etherscan.io/tx/${txHash}`;
}

export function generateAgreementHash(
  buyerAddress: string,
  sellerAddress: string,
  price: number,
  quantity: number
): string {
  // Simple hash generation - in production, use a more secure method
  const data = `${buyerAddress}-${sellerAddress}-${price}-${quantity}`;
  return data;
}
