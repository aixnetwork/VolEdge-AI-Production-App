from __future__ import annotations

from statistics import mean

from ..models import InstitutionalConfirmation, MultiTimeframeConfirmation, OhlcvBar, PatternSignal


def build_timeframe_confirmation(bars: list[OhlcvBar], direction: str) -> MultiTimeframeConfirmation:
    weekly = _trend_state(_resample(bars, 5), direction)
    daily = _trend_state(bars, direction)
    four_hour = _trend_state(bars[-56:], direction)
    aligned = sum(1 for item in (weekly, daily, four_hour) if item == "Aligned")
    score = aligned / 3 * 100
    return MultiTimeframeConfirmation(
        weekly_trend=weekly,
        daily_trend=daily,
        four_hour_trend=four_hour,
        alignment_score=round(score, 2),
    )


def build_institutional_confirmation(
    bars: list[OhlcvBar],
    benchmark: list[OhlcvBar],
    pattern: PatternSignal,
) -> InstitutionalConfirmation:
    latest = bars[-1]
    recent = bars[-14:]
    prior = bars[-56:-14]
    avg_volume = mean(bar.volume for bar in bars[-21:-1])
    rvol = latest.volume / max(1, avg_volume)
    atr_recent = mean(bar.high - bar.low for bar in recent)
    atr_prior = mean(bar.high - bar.low for bar in prior)
    atr_expansion = atr_recent / max(0.01, atr_prior)
    relative_strength = ((latest.close / bars[-20].close) - (benchmark[-1].close / benchmark[-20].close)) * 100
    ema_20 = _ema(bars, 20)
    ema_50 = _ema(bars, 50)
    ema_200 = _ema(bars, min(120, len(bars)))
    ema_alignment = 100 if latest.close > ema_20 > ema_50 > ema_200 else 72 if latest.close > ema_50 else 40
    if pattern.direction == "Bearish":
        ema_alignment = 100 if latest.close < ema_20 < ema_50 < ema_200 else 72 if latest.close < ema_50 else 40
    trend_strength = min(100, abs(latest.close - bars[-20].close) / latest.close * 700)
    band_width = (max(bar.high for bar in recent) - min(bar.low for bar in recent)) / max(0.01, latest.close) * 100
    bollinger_expansion = min(100, band_width * 12)
    sector_rotation = min(100, max(0, relative_strength * 7 + 50))
    score = (
        min(100, rvol * 55) * 0.18
        + min(100, atr_expansion * 70) * 0.18
        + sector_rotation * 0.18
        + trend_strength * 0.16
        + ema_alignment * 0.18
        + bollinger_expansion * 0.12
    )
    return InstitutionalConfirmation(
        relative_volume=round(rvol, 2),
        atr_expansion=round(atr_expansion, 2),
        relative_strength_vs_benchmark=round(relative_strength, 2),
        sector_rotation=round(sector_rotation, 2),
        trend_strength=round(trend_strength, 2),
        ema_alignment=round(ema_alignment, 2),
        bollinger_expansion=round(bollinger_expansion, 2),
        confirmation_score=round(min(100, max(0, score)), 2),
    )


def _trend_state(bars: list[OhlcvBar], direction: str) -> str:
    if len(bars) < 30 or direction == "Neutral":
        return "Mixed"
    close = bars[-1].close
    short = mean(bar.close for bar in bars[-10:])
    long = mean(bar.close for bar in bars[-30:])
    if direction == "Bearish":
        return "Aligned" if close < short < long else "Mixed" if close < long else "Against"
    return "Aligned" if close > short > long else "Mixed" if close > long else "Against"


def _resample(bars: list[OhlcvBar], window: int) -> list[OhlcvBar]:
    sampled: list[OhlcvBar] = []
    for index in range(0, len(bars), window):
        chunk = bars[index : index + window]
        if len(chunk) < window:
            continue
        sampled.append(
            OhlcvBar(
                date=chunk[-1].date,
                open=chunk[0].open,
                high=max(bar.high for bar in chunk),
                low=min(bar.low for bar in chunk),
                close=chunk[-1].close,
                volume=sum(bar.volume for bar in chunk),
            )
        )
    return sampled


def _ema(bars: list[OhlcvBar], period: int) -> float:
    values = [bar.close for bar in bars[-period:]]
    if not values:
        return bars[-1].close
    alpha = 2 / (len(values) + 1)
    ema = values[0]
    for value in values[1:]:
        ema = value * alpha + ema * (1 - alpha)
    return ema
