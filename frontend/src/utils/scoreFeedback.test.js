import { describe, expect, it } from "vitest";

import { scoreFeedback } from "./scoreFeedback";

describe("scoreFeedback", () => {
  it("returns 'Score unavailable.' for non-numeric input", () => {
    expect(scoreFeedback("not-a-number")).toBe("Score unavailable.");
    expect(scoreFeedback(NaN)).toBe("Score unavailable.");
    expect(scoreFeedback(undefined)).toBe("Score unavailable.");
  });

  it("returns near-perfect message for scores >= 85", () => {
    expect(scoreFeedback(85)).toMatch(/near-perfect/i);
    expect(scoreFeedback(99)).toMatch(/near-perfect/i);
  });

  it("returns strong-match message for scores in [70, 85)", () => {
    expect(scoreFeedback(70)).toMatch(/strong match/i);
    expect(scoreFeedback(84.9)).toMatch(/strong match/i);
  });

  it("returns decent-match message for scores in [55, 70)", () => {
    expect(scoreFeedback(55)).toMatch(/decent match/i);
    expect(scoreFeedback(69.9)).toMatch(/decent match/i);
  });

  it("returns some-elements message for scores in [40, 55)", () => {
    expect(scoreFeedback(40)).toMatch(/some elements/i);
    expect(scoreFeedback(54.9)).toMatch(/some elements/i);
  });

  it("returns off-target message for scores below 40", () => {
    expect(scoreFeedback(0)).toMatch(/off target/i);
    expect(scoreFeedback(39.9)).toMatch(/off target/i);
  });

  it("coerces numeric strings", () => {
    expect(scoreFeedback("90")).toMatch(/near-perfect/i);
    expect(scoreFeedback("0")).toMatch(/off target/i);
  });
});
