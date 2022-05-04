/**
 * @Author		FinCode s.r.l.
 * @Copyright   Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */

const fcWallet = '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1';
modal = cData1 = cData2 = mmskWallet = '';

$(function() {
    $('.js-example-basic-single').select2({
        allowClear: true,
        placeholder: 'Seleziona Cliente',
        width: 'resolve'
    });

    $(modal + ' [id^="checkbox_"]').change(function() {
        target = $(this).data('target');

        if($(this).is(':checked')) {
            $(modal + ' [id^="selectCustomer_' + target + '"]').val(null).trigger('change').prop('disabled', true);
            $(modal + ' button[type="submit"]').removeClass('w3-disabled').prop('disabled', false);
        } else {
            $(modal + ' [id^="selectCustomer_' + target + '"]').prop('disabled', false);
            $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
            resetSummary(target);
        }
    });

    $(modal + ' [id^="inputToken_"]').on('input', function() {
        $(modal + ' [id^="errorToken_"]').html('').hide();
        $(modal + ' button[type="submit"]').removeClass('w3-disabled').prop('disabled', false);

        tokenAmount = $(this).val();
        //Check number is integer and positive
        if(Math.floor(tokenAmount) == tokenAmount && Math.floor(tokenAmount) > 0 && $.isNumeric(tokenAmount)) {
            $(modal + ' button[type="submit"]').removeClass('w3-disabled').prop('disabled', false);
            
            //Check tokens disponibility
            if(modal.indexOf('CA') >= 0) {
                if(tokenAmount > cData1.tokens) {
                    $(modal + ' [id^="errorToken_"]').html('<p>Il mittente non dispone del numero di tokens indicati.</p>').show();
                    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
                }
            }
        } else {
            $(modal + ' [id^="errorToken_"]').html('<p>Indicare un numero valido di tokens da associare.</p>').show();
            $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
        }       
    });

    getLogs(false);

    $("#logType").change(function() {
        getLogs(this.checked);
    });
});

function getLogs(burned = false) {
    $.ajax({
        url: '../src/logs.php',
        data: {
            target: burned ? 'getLogsBurned' : 'getLogs',
        },
        success: function(result) {
            var table = new Tabulator("#table", {
                layout: "fitColumns",
                responsiveLayout: "collapse",
                // autoColumns: true,
                pagination: "local",
                paginationSize: 15,
                data: JSON.parse(result),
                clipboard: true,
                // autoColumnsDefinitions:function(definitions){
                //     //definitions - array of column definition objects
            
                //     definitions.forEach((column) => {
                //         column.headerFilter = true; // add header filter to every column
                //     });
            
                //     return definitions;
                // },
                columns:[
                    { title:"Seriale", field: "Seriale", headerFilter: true },
                    { title:"Token", field: "Token", headerFilter: true },
                    { title:"Nominativo", field: "Nominativo", headerFilter: true },
                    { title:"Wallet", field: "Wallet", headerFilter: true },
                    { title:"Codice Fiscale", field: "CF", headerFilter: true },
                    { title:"Partita IVA", field: "PIVA", headerFilter: true },
                    { title:"Compagnia", field: "Compagnia", headerFilter: true },
                    { title:"Download", 
                        formatter: function(cell, formatterParams){ //plain text value
                            if (!burned)
                                return "<i class='fa fa-download'></i>";
                            return "<i class='fa fa-times' style='color: red;'></i>"
                        },
                        cellClick: function(e, cell){ 
                            if (!burned) {
                                var a = document.createElement("a");
                                document.body.appendChild(a);
                                a.style = "display: none";
                                a.href = '../docs/pdf_sfp/' + cell.getRow().getData().Token + '.pdf';
                                a.download = cell.getRow().getData().Token + '.pdf';
                                a.click();
                                document.body.removeChild(a);
                            }
                        }
                    },
                ],
                // selectable: true,
            });
        },
        error: function(error) {
            console.log(error);
        }
    });    
}

function getAlert(aTitle = '', aText, aColor = 'green') {
    alert = '<div class="w3-panel w3-display-container w3-animate-opacity w3-' + aColor + '">';
    alert += '<span onclick="this.parentElement.style.display=\'none\'" class="w3-button w3-medium w3-display-topright hover-dark2">&times;</span>';
    alert += '<h4>' + aTitle + '</h4>';
    alert += '<p>' + aText + '</p>';
    alert += '</div>';
    
    $('#alerts').html(alert);
}

function resetFields() {
    $(modal + ' [id^="checkbox_"]').prop('checked', false);
    $(modal + ' [id^="selectCustomer_"]').val(null).trigger('change').prop('disabled', false);;
    $(modal + ' [id^="inputToken_"]').val('1');

    $(modal + ' [id^="loader"]').hide();
    $(modal + ' [id^="loaderText_"]').html('');
}

function resetSummary(target = 0) {
    if(target == 0) {
        cData1 = '';
    } else {
        cData2 = '';
    }

    $(modal + ' tr>td[id^="c_' + target + '"]').html('');
    $(modal + ' [id^="warning_"]').html('').hide();
    $('#errorCustomer').html('').hide();
}

function resetErrors() {
    $(modal + ' [id^="errorCustomer_"],' + modal + ' [id^="errorToken_"]').html('').hide();
    $('#alerts').html('');
}

function show_modal(item) {
    //Initialize modal
    modal = '#modal_' + item;
    mmskWallet = $('#btn_mmsk_connect').attr('data-wallet');

    if (mmskWallet == '') {
        modal = '';
        getAlert('Wallet non connesso!', 'Connetti il wallet MetaMask per utilizzare questa funzione', 'amber');
        
        return false;
    } else if (modal.indexOf('CG') >= 0 && (mmskWallet != fcWallet.toLowerCase())) {
        modal = '';
        getAlert('Wallet errato!', 'Collegarsi al wallet MetaMask FinCode per effettuare questa operazione', 'red');

        return false;
    } 

    resetFields();
    resetSummary();
    resetErrors();
    
    $(modal + ' [id^="inputToken_"]').val('1');
    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);

    $(modal + ' footer').show();
    $(modal).show();
}

function hide_modal() {
    $(modal).hide();

    modal = cData1 = cData2 = '';
}

function getCustomerData(target = 0) {
    cId = '';

    if(!$(modal + ' [id^="checkbox_' + target + '"]').is(':checked')) {
        cId = $(modal + ' [id^="selectCustomer_' + target + '"] option:selected').val();

        if(!cId) {
            $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
            resetSummary(target);
            return false;
        }
    } else {
        cId = 1;
    }

    $.ajax({
        url: '../src/ajax.php',
        dataType: 'json',
        data: {
            target: 'getCustomerData',
            id: cId
        },
        success: function(res) {
            if(target == 0) {
                cData1 = res;
            } else {
                cData2 = res;
            }
            
            $(modal + ' [id^="c_' + target + '_denomination"]').html(res.firstname + ' ' + res.lastname);
            $(modal + ' [id^="c_' + target + '_birthplace"]').html(res.birthplace);
            $(modal + ' [id^="c_' + target + '_birthdate"]').html(res.birthday);
            $(modal + ' [id^="c_' + target + '_address"]').html(res.address + ' - ' + res.postcode + ' ' + res.city + ' (' + res.province + ')');
            $(modal + ' [id^="c_' + target + '_company"]').html(res.company);
            $(modal + ' [id^="c_' + target + '_publickey"]').html(res.public_key);
            $(modal + ' [id^="c_' + target + '_tokens"]').html(res.tokens);

            $(modal + ' [id^="warning_"]').html('').hide();
            $('#errorCustomer').html('').hide();

            //Enable submit
            $(modal + ' button[type="submit"]').removeClass('w3-disabled').prop('disabled', false);
            if(modal.indexOf('CG') >= 0) {
                if(cData1.public_key == '' || cData1.public_key == null) {
                    $(modal + ' [id^="warning_"]').html('<p>Il cliente selezionato non ha alcun wallet associato</p>').show();
                    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
                }
            }

            if(modal.indexOf('CA') >= 0) {
                //Check sender/receiver not empty
                if(!cData1 || !cData2) {
                    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
                }

                //Check sender/receiver not equal
                if (cData1.id_customer == cData2.id_customer) {
                    $('#errorCustomer').html('<p>Il mittente deve essere diverso dal destinatario</p>').show();
                    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
                }

                
                submit = true;
                warnText = '';
                if (cData1 || cData2) {
                    //Check PublicKey for sender
                    if(cData1 && (cData1.public_key == '' || cData1.public_key == null)) {
                        warnText = '<p>Il mittente selezionato non ha alcun wallet associato';
                        submit = false;
                    } /*else if (cData1 && (cData1.public_key.toLowerCase() != mmskWallet)) {
                        //Check Mmsk connected with sender wallet
                        warnText = '<p>Il wallet MetaMask collegato non è quello del mittente selezionato';
                        submit = false;
                    }*/

                    //Check PublicKey for receiver
                    if(cData2 && (cData2.public_key == '' || cData2.public_key == null)) {
                        if(warnText == '') {
                            warnText = '<p>';
                        } else {
                            warnText += '<br />';
                        }
                        warnText += 'Il destinatario selezionato non ha alcun wallet associato';
                        submit = false;
                    }
                }
                warnText += '</p>';
                
                if(!submit) {
                    $(modal + ' [id^="warning_"]').html(warnText).show();
                    $(modal + ' button[type="submit"]').addClass('w3-disabled').prop('disabled', true);
                }
            }
        },
        error: function(res) {
            console.log(res);
            alert('Si è verificato un errore nella richiesta di chiamata AJAX!');
        }
    });
}

function validateForm() {
    resetErrors();

    amount = $(modal + ' [id^="inputToken_"]').val();
    cName = cData1.firstname + ' ' + cData1.lastname;
    if(modal.indexOf('CG') >= 0) {           
        var res = confirm('Confermi di voler generare ' + amount + ' tokens per il cliente: ' + cName + '?');
        if (res === true) {
            $(modal + ' [id^="loader"]').show();
            $(modal + ' footer').hide();

            generateTokens(amount);
        }
    } else if(modal.indexOf('CA') >= 0) {
        var res = confirm('Confermi di voler bruciare ' + amount + ' tokens per il cliente: ' + cName + '?');
        if (res === true) {
            $(modal + ' [id^="loader"]').show();
            $(modal + ' footer').hide();

            assignTokens(amount, true);
        }
    } else if(modal.indexOf('BR') >= 0) {
        var res = confirm('Confermi di voler bruciare ' + amount + ' tokens per il cliente: ' + cName + '?');
        if (res === true) {
            $(modal + ' [id^="loader"]').show();
            $(modal + ' footer').hide();

            assignTokens(amount, false);
        }
    }
}

function generateTokens(amount) {
    $(modal + ' [id^="loaderText_"]').html('Generazione dei PDF').show();

    $.ajax({
        url: '../src/ajax.php',
        dataType: 'json',
        data: {
            target: 'generatePDF',
            tokens: amount,
            cData: cData1
        },
        success: function(pdfs) {
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = '../docs/tmp/' + cData1.fiscalcode + '.zip';
            a.download = cData1.fiscalcode + '.zip';
            a.click();
            document.body.removeChild(a);
            
            $(modal + ' [id^="loader"]').hide();
            $(modal + ' footer').show();
        },
        error: function() {
            alert('Si è verificato un errore nella richiesta di chiamata AJAX!');
        }
    });
}

function uploadFiles(id) {
    var fd = new FormData();
    var files = $('#' + id)[0].files;

    // Check file selected or not
    if(files.length > 0) {
        for(n=0; n < files.length; n++) {
            fd.append('file[]', files[n]);
        }

        $.ajax({
            url: '../src/upload_pdf.php',
            type: 'POST',
            data: fd,
            contentType: false,
            processData: false,
            success: function(res) {
                mintTokens($.parseJSON(res));
            },
            error: function(err) {
                console.log(err)
            }
        });
    } else {
        alert("Please select a file");
    }
}

function mintTokens(pdfs) {
    //$(modal + ' [id^="loaderText_"]').html('Mint dei tokens').show();

    //Exec mint
    if(pdfs.length == 1) {
        W3_mint(pdfs);
    } else {
        nTokens = new Array(pdfs.length);
        for (i = 0; i < pdfs.length; i++) {
            nTokens[i] = 1;
        }
        W3_mint_batch(pdfs, nTokens);
    }

    //hide_modal();
}

function assignTokens(amount, toMint) {
    $(modal + ' [id^="loaderText_"]').html('Selezione dei tokens da bruciare').show();

    $.ajax({
        url: '../src/ajax.php',
        dataType: 'json',
        data: {
            target: 'getTokensToTransfer',
            id: cData1.id_customer,
            tokens: amount
        },
        success: function(ids) {
            burnTokens(ids, amount, toMint);
        },
        error: function(error) {
            console.log(error);
            alert('Si è verificato un errore nella richiesta di chiamata AJAX!');
        }
    });
}

function burnTokens(ids, amount, toMint) {
    $(modal + ' [id^="loaderText_"]').html('Burn dei tokens').show();

    var aIds = new Array(ids.length);
    var aSerials = new Array(ids.length);

    for(i=0;i<ids.length;i++) {
        thisToken = ids[i].split("_");
        aIds[i] = thisToken[0];
        aSerials[i] = thisToken[1];
    }

    //Exec transfer
    if(aIds.length == 1) {
        W3_burn(aIds);
    } else {
        nTokens = new Array(aIds.length);
        for (i = 0; i < aIds.length; i++) {
            nTokens[i] = 1;
        }
        W3_burn_batch(aIds, nTokens);
    }

    if (toMint === true) {
        $.ajax({
            url: '../src/ajax.php',
            dataType: 'json',
            data: {
                target: 'generatePDF',
                tokens: amount,
                cData: cData2,
            },
            success: function(pdfs) {
                var a = document.createElement("a");
                document.body.appendChild(a);
                a.style = "display: none";
                a.href = '../docs/tmp/' + cData2.fiscalcode + '.zip';
                a.download = cData2.fiscalcode + '.zip';
                a.click();
                document.body.removeChild(a);
                
                $(modal + ' [id^="loader"]').hide();
                $(modal + ' footer').show();
            },
            error: function(res) {
                alert('Si è verificato un errore nella richiesta di chiamata AJAX!');
            }
        });
    } else {
        $(modal + ' [id^="loader"]').hide();
        $(modal + ' footer').show();
    }
    
    //hide_modal();
}

function transferTokens(ids) {
    $(modal + ' [id^="loaderText_"]').html('Transfer dei tokens').show();

    //Exec transfer
    if(ids.length == 1) {
        W3_transfer(ids);
    } else {
        nTokens = new Array(ids.length);
        for (i = 0; i < ids.length; i++) {
            nTokens[i] = 1;
        }
        W3_transfer_batch(ids, nTokens);
    }

    hide_modal();
}