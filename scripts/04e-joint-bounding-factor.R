# Examples of the joint bound, followed by the common-ceiling optimization.
# Run from the book root: Rscript scripts/04e-joint-bounding-factor.R
ink <- '#111827'
muted <- '#6B7280'
green <- '#2F6F4E'
gold <- '#B7791F'
line <- '#C9D8CE'
wash <- '#F3F7F4'
warm <- '#F7F4EC'
E <- 2 + sqrt(2)
bound <- function(r, s) r * s / (r + s - 1)

png('images/04e-joint-bounding-factor.png',
    width = 2200, height = 1120, res = 220, pointsize = 12,
    type = 'quartz', bg = 'white')
layout(matrix(1:2, 1), widths = c(1, 1.15))
par(family = 'sans', fg = ink, col = ink, col.axis = muted,
    las = 1, mgp = c(2.8, 0.6, 0), tcl = -0.2)

# Panel 1: start with fixed association strengths.
par(mar = c(5.2, 3.4, 5.4, 1.5))
plot.new()
plot.window(xlim = c(0, 2.65), ylim = c(0.35, 4.8), xaxs = 'i', yaxs = 'i')
rect(0, 0.35, 2.65, 4.8, col = warm, border = NA)
abline(v = c(0.5, 1, 1.5, 2.5), col = 'white', lwd = 1)
segments(2, 0.35, 2, 4.6, col = gold, lty = 2, lwd = 1.8)
pairs <- rbind(c(2, 2), c(3, 3), c(3, 4), c(4, 3))
y <- 4:1
for (i in 1:4) {
  b <- bound(pairs[i, 1], pairs[i, 2])
  rect(0, y[i] - 0.16, b, y[i] + 0.16,
       col = if (b < 2) '#BACBC0' else green, border = NA)
  text(0.06, y[i] + 0.36,
       sprintf('r = %s, s = %s', pairs[i, 1], pairs[i, 2]),
       adj = 0, cex = 0.94, col = ink)
  text(b + 0.09, y[i], sprintf('%.2f', b), adj = 0,
       cex = 0.96, col = if (b < 2) muted else green)
}
text(2, 4.65, 'Observed RR = 2', adj = c(0.5, 0), col = '#765014', cex = 0.88)
axis(1, at = seq(0, 2.5, 0.5), col = line)
mtext('Largest RR the null explanation can produce', side = 1, line = 2.4, cex = 0.86)
mtext('Fix the two strengths', side = 3, line = 2.5, adj = 0,
      font = 2, col = green, cex = 1.12)
mtext('Joint bound = rs / (r + s - 1)', side = 3, line = 1.2,
      adj = 0, col = muted, cex = 0.92)

# Panel 2: allow both strengths to vary below the same ceiling t.
par(mar = c(5.2, 3.3, 5.4, 1.2))
plot.new()
plot.window(xlim = c(1, 6), ylim = c(0.9, 3.5), xaxs = 'i', yaxs = 'i')
rect(1, 0.9, 6, 3.5, col = wash, border = NA)
abline(h = c(1, 1.5, 2.5, 3), col = 'white', lwd = 1)
segments(1, 2, 6, 2, col = gold, lty = 2, lwd = 1.8)
x <- seq(1, 6, length.out = 500)
lines(x, bound(x, x), col = green, lwd = 3)
segments(E, 0.9, E, 2, col = green, lty = 3, lwd = 1.6)
points(E, 2, pch = 21, bg = gold, col = 'white', lwd = 1.7, cex = 1.6)
text(E - 0.18, 2.25, 'First reaches RR = 2', adj = 1, cex = 0.86)
text(E + 0.16, 1.22, 'E-value', adj = 0, font = 2, col = green, cex = 0.95)
text(E + 0.16, 1.05, expression(2 + sqrt(2) == 3.414), adj = 0, col = green, cex = 0.86)
text(5.85, 2.10, 'Observed RR = 2', adj = 1, col = '#765014', cex = 0.88)
text(4.95, 3.15, expression(t^2 / (2*t-1)), adj = 1, col = green, cex = 0.95)
axis(1, at = 1:6, col = line)
axis(2, at = seq(1, 3.5, 0.5), col = line)
mtext('Common ceiling t on both r and s', side = 1, line = 2.4, cex = 0.9)
mtext('Largest RR', side = 2, line = 2.2, las = 0, cex = 0.86)
mtext('Find the smallest shared ceiling', side = 3, line = 2.5,
      adj = 0, font = 2, col = green, cex = 1.12)
mtext('If r and s are at most t, the maximum occurs at r = s = t',
      side = 3, line = 1.2, adj = 0, col = muted, cex = 0.80)
dev.off()
