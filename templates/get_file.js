const CORSPROXY = 'https://secure-ocean-87335.herokuapp.com/';

$('.ls-btn-submit').on('click', (e) => {
	e.preventDefault();
	console.log('fire on-click for .ls-btn-submit');
	getDocument(e);
});

$('#searchLawByAssocBill').on('click', (e) => {
	e.preventDefault();
	$('#formGetLawByAssocBill').show();
	$('#formGetLawByNumber').hide();
});

$('#searchLawByNumber').on('click', (e) => {
	e.preventDefault();
	$('#formGetLawByNumber').show();
	$('#formGetLawByAssocBill').hide();
});

// fix close buttons on alert modal not hiding on click
$('#alertModal button[data-dismiss="modal"]').each(() => {
	$(this).on('click', () => {
		$('#alertModal').modal('hide');
	});
});

function buildRequest(e) {
	('use strict');
	console.log('start function buildRequest()');

	const $target = $(e.currentTarget);
	console.log('const $target is:');
	console.log($target);

	const $form = $target.closest('.ls-form');
	console.log('const $form is:');
	console.log($form);

	const targetDoc = $form.attr('data-ls-target-doc');
	const targetDocDesc = $form.attr('data-ls-target-doc-desc');
	console.log(`const targetDoc is ${targetDoc}`);
	console.log(`const targetDocDesc is ${targetDocDesc}`);

	// get inputs
	const $docCongress = $form.find('.ls-form-select-doccongress');
	const $docType = $form.find('.ls-form-select-doctype');
	const $docNumber = $form.find('.ls-form-input-docnumber');
	console.log('const $docCongress is:');
	console.log($docCongress);
	console.log('const $docType is:');
	console.log($docType);
	console.log('const $docNumber is:');
	console.log($docNumber);

	// get values for govinfo link service
	const docCongress = $docCongress.val();
	const docType = $docType.val();
	const docNumber = $docNumber.val();
	console.log(`const docCongress is ${docCongress}`);
	console.log(`const docType is ${docType}`);
	console.log(`const docNumber is ${docNumber}`);

	// if version not selected then set to enrolled

	// get selected options for dropdowns
	const selectedCongress = $docCongress[0].selectedIndex;
	const selectedType = $docType[0].selectedIndex;
	console.log(`const selectedCongress is ${selectedCongress}`);
	console.log(`const selectedType is ${selectedType}`);

	// get text values for error message
	const docCongressText = $docCongress[0].options[selectedCongress].text;
	const docTypeText = $docType[0].options[selectedType].text;
	const docNumberText = $docNumber[0].value;
	console.log(`const docCongressText is ${docCongressText}`);
	console.log(`const docTypeText is ${docTypeText}`);
	console.log(`const docNumberText is ${docNumberText}`);

	// get values for doc version if target doc is bill
	let docVersion, docVersionText;
	if (targetDoc === 'bill') {
		const $docVersion = $form.find('.ls-form-select-docversion');
		console.log('const $docVersion is:');
		console.log($docVersion);
		docVersion = $docVersion.val();
		if (docVersion.length < 1) {
			$docVersion[0].selectedIndex = 1;
		}
		docVersion = $docVersion.val();
		console.log(`const docVersion is ${docVersion}`);
		const selectedVersion = $docVersion[0].selectedIndex;
		console.log(`const selectedVersion is ${selectedVersion}`);
		docVersionText = $docVersion[0].options[selectedVersion].text;
		console.log(`const docVersionText is ${docVersionText}`);
	}

	// build url paths for govinfo link service
	let url = 'https://www.govinfo.gov/link/';
	switch (targetDoc) {
		case 'bill':
			url += `bills/${docCongress}/${docType}/${docNumber}?billversion=${docVersion}&link-type=uslm`;
			break;
		case 'law':
			url += `plaw/${docCongress}/${docType}/${docNumber}?link-type=uslm`;
			break;
		case 'lawassocbill':
			url += `plaw/${docCongress}/${encodeURIComponent(
				docType + ' ' + docNumber
			)}?link-type=uslm`;
			break;
		default:
			console.log('const type is none of bill, law, or lawassocbill');
			return false;
	}

	// return url and text values for error message
	const $getRequest = {
		url: url,
		targetDocDesc: targetDocDesc,
		docCongressText: docCongressText,
		docTypeText: docTypeText,
		docNumberText: docNumberText,
		docVersionText: docVersionText ? docVersionText : '',
	};

	console.log('end function buildRequest()');
	return $getRequest;
}

function getDocument(e) {
	console.log('start function getDocument()');

	const $getRequest = buildRequest(e);
	console.log('const getRequest is:');
	console.log($getRequest);

	const { url } = $getRequest;
	const { targetDocDesc } = $getRequest;
	const { docCongressText } = $getRequest;
	const { docTypeText } = $getRequest;
	const { docNumberText } = $getRequest;
	const { docVersionText } = $getRequest;
	const urlAjax = `${CORSPROXY}${url}`;
	console.log(`const url is ${url}`);
	console.log(`const docCongressText is ${docCongressText}`);
	console.log(`const docTypeText is ${docTypeText}`);
	console.log(`const docNumberText is ${docNumberText}`);
	console.log(`const docVersionText is ${docVersionText}`);
	console.log(`const urlAjax is ${urlAjax}`);

	$.ajax({
		url: urlAjax,
		dataType: 'html',
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			accept: '*/*',
		},
		success(data, status, xhr) {
			console.log('start callback for getDocument()');

			console.log('data is:');
			console.log(data);
			console.log(`textStatus is ${status}`);
			console.log('xhr is:');
			console.log(xhr);

			$('#file').text(data);

			console.log('end callback for getDocument()');
			return data;
		},
		error(xhr, status, error) {
			console.log('xhr is:');
			console.log(xhr);
			console.log(`textStatus is ${status}`);
			console.log('error is:');
			console.log(error);
			let modalHtml = `<p>No ${targetDocDesc} was found matching the following description:</p>
			<ul>
			<li>Congress:  ${docCongressText}</li>
			<li>Document Type:  ${docTypeText}</li>
			<li>Document Number:  ${docNumberText}</li>`;
			modalHtml +=
				docVersionText.length > 0
					? `<li>Bill Version:  ${docVersionText}</li>`
					: '';
			modalHtml += `</ul>
			<p>Please check the citation and try again or <a href="mailto:jeffrey.sharer@lexshift.com">contact us</a>.</p>`;
			$('#alertModal').find('.modal-body').html(modalHtml);
			$('#alertModal').modal('show');
		},
	});

	console.log('end function getDocument()');
}
