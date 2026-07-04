# Part 2 Real-Multiplier Gate

## Result

Uniform contraction of the manuscript's genuine return blocks is false.

For a return block,
\[
2^{b+2d}t'=3^{b+d}t+E_{b,d},\qquad E_{b,d}=3^{d-1}(3^b-2^b)>0.
\]
Thus its linear multiplier is
\[
A_{b,d}=\frac{3^{b+d}}{2^{b+2d}}=\left(\frac32\right)^b\left(\frac34\right)^d.
\]

Take \(t=5\). Then
\[
3t+1=16=2^4\cdot1,
\qquad
3^4\cdot1-1=80=2^4\cdot5.
\]
Hence \(b=4\), \(d=2\), and
\[
t'=3^{d-1}\cdot5=15.
\]
The exact block identity is
\[
2^8\cdot15=3^6\cdot5+3(3^4-2^4)=3645+195=3840,
\]
so
\[
\boxed{t'/t=3>1.}
\]

Therefore neither every block nor every return block has negative drift.

## New gate

Any viable real-dynamics argument must control whole admissible words:
\[
\sum_{i=1}^N(s_i\log3-m_i\log2)
\]
together with the accumulated affine terms. It must use a proved restriction on the actual valuation language; shell membership and positivity of constants are not enough.

## Status

\[
\text{uniform per-block contraction}\quad [██████████]\ 100\%\ \text{disproved}
\]
\[
\text{long-word exceptional-language theorem}\quad [░░░░░░░░░░]\ 0\%
\]
\[
\text{no-divergence theorem}\quad [░░░░░░░░░░]\ 0\%
\]
