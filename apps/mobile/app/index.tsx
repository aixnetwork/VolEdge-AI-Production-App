import { Link } from "expo-router";
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";

const top = {
  symbol: "UVIX",
  score: 91,
  accuracy: 67,
  matches: 84,
  return: "+8.4%",
  window: "3-5 trading days",
  entry: "14.80",
  stop: "13.45",
  target: "18.20",
  explanation: "Volatility expansion is accelerating while matching historical setups show the strongest short-window payoff profile."
};

const ranked = [
  ["SOXL", 86, "Strong Buy"],
  ["GLD", 82, "Strong Buy"],
  ["XBI", 77, "Watch"]
] as const;

export default function RadarScreen() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.brand}>VolEdge AI</Text>
      <Text style={styles.title}>Opportunity Radar</Text>

      <View style={styles.nav}>
        {["Sectors", "Alerts", "Watchlist", "Risk"].map((item) => (
          <Link key={item} href={`/${item.toLowerCase()}`} style={styles.navItem}>
            {item}
          </Link>
        ))}
      </View>

      <View style={styles.hero}>
        <View style={styles.row}>
          <View>
            <Text style={styles.label}>Top Opportunity</Text>
            <Text style={styles.symbol}>{top.symbol}</Text>
          </View>
          <View style={styles.scoreBox}>
            <Text style={styles.label}>VolEdge Score</Text>
            <Text style={styles.score}>{top.score}</Text>
          </View>
        </View>

        <View style={styles.metrics}>
          <Metric label="Accuracy" value={`${top.accuracy}%`} />
          <Metric label="Matches" value={String(top.matches)} />
          <Metric label="Return" value={top.return} />
          <Metric label="Window" value={top.window} />
        </View>

        <Text style={styles.explanation}>{top.explanation}</Text>

        <View style={styles.tradePlan}>
          <Metric label="Entry" value={top.entry} />
          <Metric label="Stop" value={top.stop} />
          <Metric label="Target" value={top.target} />
        </View>

        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>Manual Approval</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.sectionTitle}>Top Ranked ETFs</Text>
      {ranked.map(([symbol, score, signal]) => (
        <View key={symbol} style={styles.card}>
          <View>
            <Text style={styles.cardSymbol}>{symbol}</Text>
            <Text style={styles.label}>{signal}</Text>
          </View>
          <Text style={styles.cardScore}>{score}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.metric}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.metricValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#080b10" },
  content: { padding: 20, paddingTop: 58 },
  brand: { color: "#34d399", fontWeight: "700", fontSize: 14 },
  title: { color: "#f7fbff", fontSize: 30, fontWeight: "800", marginTop: 4, marginBottom: 18 },
  nav: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 14 },
  navItem: { color: "#34d399", borderColor: "#243241", borderWidth: 1, borderRadius: 6, paddingHorizontal: 12, paddingVertical: 8, fontWeight: "800" },
  hero: { borderWidth: 1, borderColor: "#243241", backgroundColor: "#101820", borderRadius: 8, padding: 18 },
  row: { flexDirection: "row", justifyContent: "space-between", gap: 12 },
  label: { color: "#8ca3b7", fontSize: 12, textTransform: "uppercase" },
  symbol: { color: "#fff", fontSize: 56, fontWeight: "900" },
  scoreBox: { alignItems: "flex-end" },
  score: { color: "#34d399", fontSize: 76, fontWeight: "900", lineHeight: 82 },
  metrics: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 16 },
  metric: { minWidth: "45%", flex: 1 },
  metricValue: { color: "#fff", fontSize: 22, fontWeight: "800", marginTop: 4 },
  explanation: { color: "#d9e6ef", lineHeight: 23, marginTop: 18, fontSize: 15 },
  tradePlan: { flexDirection: "row", gap: 10, marginTop: 18 },
  button: { backgroundColor: "#34d399", borderRadius: 6, height: 50, alignItems: "center", justifyContent: "center", marginTop: 18 },
  buttonText: { color: "#080b10", fontWeight: "900", fontSize: 16 },
  sectionTitle: { color: "#fff", fontSize: 20, fontWeight: "800", marginTop: 24, marginBottom: 10 },
  card: { borderWidth: 1, borderColor: "#243241", borderRadius: 8, backgroundColor: "#101820", padding: 16, marginBottom: 10, flexDirection: "row", justifyContent: "space-between" },
  cardSymbol: { color: "#fff", fontSize: 28, fontWeight: "900" },
  cardScore: { color: "#34d399", fontSize: 42, fontWeight: "900" }
});
