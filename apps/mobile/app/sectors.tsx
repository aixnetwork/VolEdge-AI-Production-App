import { ScrollView, StyleSheet, Text, View } from "react-native";

const sectors = [
  ["Volatility", "UVIX", 94, "Extreme Buy"],
  ["Semiconductors", "SOXX", 88, "Strong Buy"],
  ["Gold Miners", "GDX", 80, "Strong Buy"],
  ["Energy", "XLE", 54, "Watch"]
] as const;

export default function Sectors() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Sector Volatility Radar</Text>
      {sectors.map(([sector, symbol, score, signal]) => (
        <View key={symbol} style={styles.card}>
          <View>
            <Text style={styles.label}>{sector}</Text>
            <Text style={styles.symbol}>{symbol}</Text>
          </View>
          <View style={styles.right}>
            <Text style={styles.score}>{score}</Text>
            <Text style={styles.label}>{signal}</Text>
          </View>
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
  label: { color: "#8ca3b7", fontSize: 12, textTransform: "uppercase" },
  symbol: { color: "#fff", fontSize: 32, fontWeight: "900" },
  right: { alignItems: "flex-end" },
  score: { color: "#34d399", fontSize: 44, fontWeight: "900" }
});
