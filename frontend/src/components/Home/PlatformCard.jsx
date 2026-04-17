import styles from "./PlatformCard.module.css";

export default function PlatformCard({ children, className = "" }) {
  return <div className={`${styles.platformCard} ${className}`}>{children}</div>;
}