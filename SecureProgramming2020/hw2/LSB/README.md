## LSB
This challenge is slightly different from the classic LSB oracle. Instead of leaking the least significant bit, we got the decrypted value modulo three.

I've tried to expand the original LSB oracle to mod three. That is,
$\lfloor\lfloor3m\rfloor_n\rfloor_3 = \lfloor3m\rfloor_3 = 0 \ \ \ \ if\ \ \ \  m \in [0,\frac{n}{3})$
$\lfloor\lfloor3m\rfloor_n\rfloor_3 = \lfloor3m-n\rfloor_3 = \lfloor-n\rfloor_3 \ \ \ \ if\ \ \ \  m \in [\frac{n}{3},\frac{2n}{3})$
$\lfloor\lfloor3m\rfloor_n\rfloor_3 = \lfloor3m-2n\rfloor_3 = \lfloor-2n\rfloor_3 \ \ \ \ if\ \ \ \  m \in [\frac{2n}{3},1)$

Note that we are not sure about the value in range $[\frac{n}{3},\frac{2n}{3})$ and range $[\frac{2n}{3},1)$ since `n` is unknown at this point. However, this is not the case since we'll get `n` when we connect to the server.

To solve this challenge, we can simply write a **ternary** search method.
The script can be found at [solve.py](./solve.py)
