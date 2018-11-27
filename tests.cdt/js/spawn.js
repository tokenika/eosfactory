// var dialog = require('nw-dialog')
// dialog.setContext(document) // work in client
// dialog.openFileDialog(function(result) {
//     alert(result)
// })


// const child_process = require("child_process")
// function systemSync(cmd){
//     child_process.exec(
//         cmd, 
//         (err, stdout, stderr) => {
//         console.log('stdout is:' + stdout)
//         console.log('stderr is:' + stderr)
//         console.log('error is:' + err)
//     }).on(
//         'exit', 
//         (code) => {console.log('final exit code is', code)}
//         )
// }

// systemSync('ls')

const child_process = require("child_process");
((cmd) => {
    child_process.exec(
        cmd, 
        (err, stdout, stderr) => {
        console.log('stdout is:' + stdout)
        console.log('stderr is:' + stderr)
        console.log('error is:' + err)
    }).on(
        'exit', 
        (code) => {console.log('final exit code is', code)}
        )
})('ls')


