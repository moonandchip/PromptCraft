import { useEffect, useState } from "react";
import { getHealth } from "../api";

export default function CheckHealth() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    getHealth().then((data) => {
      if (data) {
        setStatus("API Health: GOOD");
      } else {
        setStatus("API Health: BAD");
      }
    });
  }, []);

  return <div>{status}</div>;
}
