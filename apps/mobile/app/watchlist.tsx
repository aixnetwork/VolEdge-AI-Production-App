import { ScrollView, StyleSheet, Text, View } from "react-native";

const watchlist = [
  ["UVIX", 91, "Extreme Buy"],
  ["SOXL", 86, "Strong Buy"],
  ["GLD", 82, "Strong Buy"],
  ["XBI", 77, "Watch"]
] as const;

export default function Watchlist() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Watchlist</Text>
      {watchlist.map(([symbol, score, signal]) => (
        <View key={symbol} style={styles.card}>
          <View>
            <Text style={styles.symbol}>{symbol}</Text>
            <Text style={styles.label}>{signal}</Text>
          </View>
          <Text style={styles.score}>{score}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#080b10" },
  content: { padding: 20, paddingTop: 58 },
  title: { color: "#fff", fontSize: 28, fontWeight: "900", marginBottom: 18 },
  card: { borderWidth: 1, borderColor: "#243241", borderRadius: 8, backgroundColor: "#101820", padding: 16, marginBottom: 10, flexDirection: "row", justifyContent: "space-between" },
  symbol: { color: "#fff", fontSize: 30, fontWeight: "900" },
  label: { color: "#8ca3b7", fontSize: 12, textTransform: "uppercase" },
  score: { color: "#34d399", fontSize: 44, fontWeight: "900" }
});
