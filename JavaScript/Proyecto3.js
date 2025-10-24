const readline = require('readline');
const { execSync } = require('child_process');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const TAMANO = 10;
const BARCOS = [
  { nombre: 'Portaaviones', tamaño: 5, simbolo: 'P' },
  { nombre: 'Acorazado', tamaño: 4, simbolo: 'A' },
  { nombre: 'Crucero', tamaño: 3, simbolo: 'C' },
  { nombre: 'Submarino', tamaño: 3, simbolo: 'S' },
  { nombre: 'Destructor', tamaño: 2, simbolo: 'D' }
];

function crearTablero() {
  let grid = [];
  for (let i = 0; i < TAMANO; i++) {
    grid.push(Array(TAMANO).fill('~'));
  }
  return grid;
}

function crearDisparos() {
  let d = [];
  for (let i = 0; i < TAMANO; i++) d.push(Array(TAMANO).fill(false));
  return d;
}

function mostrarTablero(grid, disparos, barcos, ocultarBarcos) {
  console.log('\n  ' + 'ABCDEFGHIJ'.split('').join(' '));
  for (let i = 0; i < TAMANO; i++) {
    let fila = (i + 1).toString().padStart(2) + ' ';
    for (let j = 0; j < TAMANO; j++) {
      if (disparos[i][j]) {
        if (grid[i][j] === '~') fila += 'O ';
        else {
          let barco = barcos.find(b => b.posiciones.some(p => p[0] === i && p[1] === j));
          fila += barco.impactos === barco.tamaño ? '🔥 ' : 'X ';
        }
      } else if (ocultarBarcos && grid[i][j] !== '~') {
        fila += '~ ';
      } else {
        fila += grid[i][j] + ' ';
      }
    }
    console.log(fila);
  }
  console.log('\nLeyenda: ~ = Agua, O = Fallo, X = Impacto, 🔥 = Hundido\n');
}

function puedeColocar(grid, fila, col, tamaño, horizontal) {
  if (horizontal) {
    if (col + tamaño > TAMANO) return false;
    for (let i = 0; i < tamaño; i++) if (grid[fila][col + i] !== '~') return false;
  } else {
    if (fila + tamaño > TAMANO) return false;
    for (let i = 0; i < tamaño; i++) if (grid[fila + i][col] !== '~') return false;
  }
  return true;
}

function colocarBarco(grid, barcos, fila, col, barco, horizontal) {
  let posiciones = [];
  for (let i = 0; i < barco.tamaño; i++) {
    let r = horizontal ? fila : fila + i;
    let c = horizontal ? col + i : col;
    grid[r][c] = barco.simbolo;
    posiciones.push([r, c]);
  }
  barcos.push({ ...barco, posiciones, impactos: 0 });
}

function disparar(grid, disparos, barcos, fila, col) {
  if (disparos[fila][col]) return { valido: false, msg: 'Ya disparaste aquí' };
  disparos[fila][col] = true;
  if (grid[fila][col] === '~') return { valido: true, impacto: false, msg: 'Agua!' };
  let barco = barcos.find(b => b.posiciones.some(p => p[0] === fila && p[1] === col));
  barco.impactos++;
  if (barco.impactos === barco.tamaño) return { valido: true, impacto: true, hundido: true, msg: `¡Hundiste el ${barco.nombre}!` };
  return { valido: true, impacto: true, msg: '¡Impacto!' };
}

function todosHundidos(barcos) {
  return barcos.every(b => b.impactos === b.tamaño);
}

function pregunta(q) {
  return new Promise(res => rl.question(q, res));
}

function coordenadasAIndices(coord) {
  if (coord.length < 2) return null;
  let col = coord[0].toUpperCase().charCodeAt(0) - 65;
  let fila = parseInt(coord.slice(1)) - 1;
  if (col < 0 || col >= TAMANO || fila < 0 || fila >= TAMANO) return null;
  return [fila, col];
}

function limpiarPantalla() {
  try { execSync('cls', {stdio: 'inherit'}); } catch {}
}

async function colocarBarcosJugador(grid, barcos, nombre) {
  console.log(`\n=== ${nombre.toUpperCase()}: COLOCA TUS BARCOS ===\n`);
  for (let barco of BARCOS) {
    let colocado = false;
    while (!colocado) {
      mostrarTablero(grid, crearDisparos(), barcos, false);
      console.log(`\nColoca tu ${barco.nombre} (tamaño: ${barco.tamaño})`);
      let coord = await pregunta('Coordenada inicial (ej: A1): ');
      let indices = coordenadasAIndices(coord);
      if (!indices) { console.log('Coordenada inválida.'); continue; }
      let orientacion = await pregunta('Orientación (H=horizontal, V=vertical): ');
      let horizontal = orientacion.toUpperCase() === 'H';
      if (puedeColocar(grid, indices[0], indices[1], barco.tamaño, horizontal)) {
        colocarBarco(grid, barcos, indices[0], indices[1], barco, horizontal);
        colocado = true;
      } else {
        console.log('No se puede colocar el barco ahí.');
      }
    }
  }
  console.log(`\n¡${nombre}, todos tus barcos han sido colocados!\n`);
  mostrarTablero(grid, crearDisparos(), barcos, false);
  await pregunta('Presiona Enter para continuar...');
  limpiarPantalla();
}

async function jugar() {
  console.log('=== BATALLA NAVAL 2 JUGADORES ===');
  let jugador1 = await pregunta('Nombre del Jugador 1: ');
  let jugador2 = await pregunta('Nombre del Jugador 2: ');
  await pregunta('\nPresiona Enter para comenzar a colocar los barcos...');
  limpiarPantalla();

  let grid1 = crearTablero(), grid2 = crearTablero();
  let barcos1 = [], barcos2 = [];
  let disparos1 = crearDisparos(), disparos2 = crearDisparos();

  console.log(`${jugador2}, por favor aparta la vista...`);
  await pregunta('Presiona Enter cuando estés listo...');
  limpiarPantalla();
  await colocarBarcosJugador(grid1, barcos1, jugador1);

  console.log(`${jugador1}, por favor aparta la vista...`);
  await pregunta('Presiona Enter cuando estés listo...');
  limpiarPantalla();
  await colocarBarcosJugador(grid2, barcos2, jugador2);

  let turno = Math.random() < 0.5 ? 1 : 2;
  let numTurno = 1;
  await pregunta('Presiona Enter para comenzar la batalla...');
  while (true) {
    limpiarPantalla();
    let jActual = turno === 1 ? jugador1 : jugador2;
    let gridPropio = turno === 1 ? grid1 : grid2;
    let gridEnemigo = turno === 1 ? grid2 : grid1;
    let barcosPropios = turno === 1 ? barcos1 : barcos2;
    let barcosEnemigos = turno === 1 ? barcos2 : barcos1;
    let disparosPropios = turno === 1 ? disparos1 : disparos2;
    let nombreEnemigo = turno === 1 ? jugador2 : jugador1;

    console.log(`\n=== TURNO ${numTurno} - ${jActual.toUpperCase()} ===\n`);
    console.log('TU TABLERO:');
    mostrarTablero(gridPropio, crearDisparos(), barcosPropios, false);
    console.log(`\nTABLERO DE ${nombreEnemigo.toUpperCase()}:`);
    mostrarTablero(gridEnemigo, disparosPropios, barcosEnemigos, true);

    let disparoValido = false;
    while (!disparoValido) {
      let coord = await pregunta(`\n${jActual}, tu disparo (ej: B5): `);
      let indices = coordenadasAIndices(coord);
      if (!indices) { console.log('Coordenada inválida.'); continue; }
      let res = disparar(gridEnemigo, disparosPropios, barcosEnemigos, indices[0], indices[1]);
      if (res.valido) {
        console.log(`\n${res.msg}`);
        disparoValido = true;
        if (todosHundidos(barcosEnemigos)) {
          console.log(`\n🎉 ¡${jActual.toUpperCase()} GANA!`);
          rl.close();
          return;
        }
        await pregunta(`\nPresiona Enter para pasar el turno a ${nombreEnemigo}...`);
      } else {
        console.log(res.msg);
      }
    }
    turno = turno === 1 ? 2 : 1;
    numTurno++;
  }
}

jugar();